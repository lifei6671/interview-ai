package server

import (
	"context"
	"errors"
	"fmt"
	"io"
	"log"
	"net"
	"net/http"
	"net/http/httputil"
	"os"
	"runtime/debug"
	"strings"
	"sync/atomic"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/lifei6671/logit"
	"go.uber.org/zap"
)

var (
	// DefaultMaxBodyBytes 默认最大请求体大小,默认32M
	DefaultMaxBodyBytes int64 = 1024 * 1024 * 32
	// DefaultMaxHeaderBytes 默认最大请求头大小,默认1M
	DefaultMaxHeaderBytes = 1024 * 1024 * 1
)

// Server 服务接口
type Server interface {
	Serve(l net.Listener) error
	RegisterOnShutdown(f func())
	SetKeepAlivePeriod(d time.Duration)
	Shutdown(ctx context.Context) error
	AddRoute(httpMethod, relativePath string, handler gin.HandlerFunc)
	GetHandler() http.Handler

	Router() gin.IRoutes
	Engine() *gin.Engine
}

type Option func(*DefaultServer)

// WithReadTimeout 设置读超时
func WithReadTimeout(d time.Duration) Option {
	return func(s *DefaultServer) { s.ReadTimeout = d }
}

// WithWriteTimeout 设置写超时
func WithWriteTimeout(d time.Duration) Option {
	return func(s *DefaultServer) { s.WriteTimeout = d }
}

// WithMaxBodyBytes 设置最大请求体大小
func WithMaxBodyBytes(n int64) Option {
	return func(s *DefaultServer) { s.MaxBodyBytes = n }
}

// WithMaxHeaderBytes 设置最大请求头大小
func WithMaxHeaderBytes(n int64) Option {
	return func(s *DefaultServer) {
		if n <= 0 {
			s.MaxHeaderBytes = 0
			return
		}
		// 安全转换：避免 int 溢出
		maxInt := int64(^uint(0) >> 1)
		if n > maxInt {
			s.MaxHeaderBytes = int(maxInt)
			return
		}
		s.MaxHeaderBytes = int(n)
	}
}

// WithLogitLogger 注入日志组件（强烈建议必传）
func WithLogitLogger(lg *logit.Logger) Option {
	return func(s *DefaultServer) { s.Logger = lg }
}

// WithRecoveryAllowSensitiveDump 控制 recovery 是否允许输出敏感 header（默认 false）
func WithRecoveryAllowSensitiveDump(allow bool) Option {
	return func(s *DefaultServer) { s.allowSensitiveDump = allow }
}

// WithServerErrorLogStack 控制 http.Server.ErrorLog 是否携带 stack（默认 false）
func WithServerErrorLogStack(enable bool) Option {
	return func(s *DefaultServer) { s.serverErrorLogStack = enable }
}

type DefaultServer struct {
	s      *gin.Engine
	server *http.Server

	ReadTimeout  time.Duration
	WriteTimeout time.Duration

	// 最大请求体大小（-1 回退默认；0 不限制/不启用 MaxBytesReader）
	MaxBodyBytes int64

	// 最大请求头大小（-1 回退默认；0 使用 http.Server 默认行为）
	MaxHeaderBytes int

	Logger *logit.Logger

	// 内部控制项
	allowSensitiveDump  bool
	serverErrorLogStack bool
	served              atomic.Bool // Serve() 调用后置 true，禁止再 AddRoute
}

func (s *DefaultServer) Engine() *gin.Engine {
	return s.s
}
func (s *DefaultServer) Router() gin.IRoutes {
	return s.s
}

func New(ctx context.Context, addr string, options ...Option) Server {
	s := DefaultServer{
		MaxBodyBytes:   DefaultMaxBodyBytes,
		MaxHeaderBytes: DefaultMaxHeaderBytes,
	}

	for _, option := range options {
		option(&s)
	}

	if s.MaxBodyBytes == -1 {
		s.MaxBodyBytes = DefaultMaxBodyBytes
	}
	if s.MaxHeaderBytes == -1 {
		s.MaxHeaderBytes = DefaultMaxHeaderBytes
	}

	// 这里选择“硬失败”：因为 logger 缺失会导致中间件 NPE 或静默丢日志
	if s.Logger == nil {
		panic("server.New: Logger is nil; please provide WithLogitLogger(...)")
	}

	engine := gin.New()
	engine.ContextWithFallback = true
	engine.Use(
		GinWithContextMeta(DefaultContextMetaOptions()),
		ginWithLogger(s.Logger),
		ginWithRecovery(s.Logger, true, s.allowSensitiveDump),
	)

	// body 限制：只对常见有 body 的方法启用，避免误伤
	if s.MaxBodyBytes > 0 {
		engine.Use(func(c *gin.Context) {
			switch c.Request.Method {
			case http.MethodPost, http.MethodPut, http.MethodPatch:
				c.Request.Body = http.MaxBytesReader(c.Writer, c.Request.Body, s.MaxBodyBytes)
			}
			c.Next()
		})
	}

	s.s = engine
	s.server = &http.Server{
		Addr:           addr,
		Handler:        engine.Handler(),
		ReadTimeout:    s.ReadTimeout,
		WriteTimeout:   s.WriteTimeout,
		MaxHeaderBytes: s.MaxHeaderBytes,
		BaseContext: func(listener net.Listener) context.Context {
			return ctx
		},
		ErrorLog: log.New(&logitWriter{
			logger:    s.Logger,
			ctx:       ctx,
			withStack: s.serverErrorLogStack,
		}, "", log.LstdFlags),
	}

	return &s
}

func (s *DefaultServer) Serve(l net.Listener) error {
	if s.server == nil {
		return errors.New("server not initialized")
	}
	s.served.Store(true)
	return s.server.Serve(l)
}

func (s *DefaultServer) RegisterOnShutdown(f func()) {
	if s.server == nil || f == nil {
		return
	}
	s.server.RegisterOnShutdown(f)
}

// SetKeepAlivePeriod 注意：这里设置的是 http.Server.IdleTimeout（HTTP keep-alive 空闲连接超时），不是 TCP keepalive probe 周期。
// d==0 会关闭 keep-alive
func (s *DefaultServer) SetKeepAlivePeriod(d time.Duration) {
	if s.server == nil {
		return
	}
	if d == 0 {
		s.server.SetKeepAlivesEnabled(false)
		return
	}
	s.server.SetKeepAlivesEnabled(true)
	s.server.IdleTimeout = d
}

func (s *DefaultServer) Shutdown(ctx context.Context) error {
	if s.server == nil {
		return nil
	}
	return s.server.Shutdown(ctx)
}

func (s *DefaultServer) AddRoute(httpMethod, relativePath string, handler gin.HandlerFunc) {
	// 防止运行中动态加路由（Gin 路由树并发安全不可依赖）
	if s.served.Load() {
		panic(fmt.Sprintf("server.AddRoute called after Serve started: %s %s", httpMethod, relativePath))
	}
	s.s.Handle(httpMethod, relativePath, handler)
}

func (s *DefaultServer) GetHandler() http.Handler {
	if s.server != nil && s.server.Handler != nil {
		return s.server.Handler
	}
	return s.s.Handler()
}

// logitWriter 将 logit.Logger 适配为 io.Writer，以对接标准库 *log.Logger（http.Server.ErrorLog）
type logitWriter struct {
	logger    *logit.Logger
	ctx       context.Context
	withStack bool
}

func (e *logitWriter) Write(p []byte) (n int, err error) {
	if e.logger == nil {
		return len(p), nil
	}
	msg := strings.TrimSpace(string(p))
	if msg == "" {
		return len(p), nil
	}

	fields := make([]zap.Field, 0, 2)
	if e.withStack {
		fields = append(fields, zap.String("stack", string(debug.Stack())))
	}
	e.logger.Warn(e.ctx, msg, fields...)
	return len(p), nil
}

var _ io.Writer = (*logitWriter)(nil)

// ginWithLogger 接收 gin 框架日志
func ginWithLogger(lg *logit.Logger) gin.HandlerFunc {
	return func(c *gin.Context) {
		start := time.Now()
		path := c.Request.URL.Path
		query := c.Request.URL.RawQuery

		c.Next()

		if lg == nil {
			return
		}

		cost := time.Since(start)
		ctx := c.Request.Context()

		lg.Info(ctx,
			path,
			zap.Int("status", c.Writer.Status()),
			zap.String("method", c.Request.Method),
			zap.String("path", path),
			zap.String("query", query),
			zap.String("ip", c.ClientIP()),
			zap.String("user-agent", c.Request.UserAgent()),
			zap.String("errors", c.Errors.String()),
			zap.Duration("cost", cost),
		)
	}
}

// ginWithRecovery recover 掉 panic 并记录日志
// allowSensitiveDump=false 时，输出脱敏的请求摘要，避免泄露 Authorization/Cookie 等
func ginWithRecovery(lg *logit.Logger, stack bool, allowSensitiveDump bool) gin.HandlerFunc {
	return func(c *gin.Context) {
		defer func() {
			if rec := recover(); rec != nil {
				var brokenPipe bool

				if e, ok := rec.(error); ok && e != nil {
					var ne *net.OpError
					if errors.As(e, &ne) {
						var se *os.SyscallError
						if errors.As(ne.Err, &se) {
							msg := strings.ToLower(se.Error())
							if strings.Contains(msg, "broken pipe") || strings.Contains(msg, "connection reset by peer") {
								brokenPipe = true
							}
						}
					}
				}

				ctx := c.Request.Context()

				var reqDump string
				if allowSensitiveDump {
					if b, err := httputil.DumpRequest(c.Request, false); err == nil {
						reqDump = string(b)
					} else {
						reqDump = safeRequestDump(c.Request)
					}
				} else {
					reqDump = safeRequestDump(c.Request)
				}

				if lg == nil {
					if brokenPipe {
						c.Abort()
						return
					}
					c.AbortWithStatus(http.StatusInternalServerError)
					return
				}

				if brokenPipe {
					lg.Error(ctx,
						c.Request.URL.Path,
						zap.Any("error", rec),
						zap.String("request", reqDump),
					)
					// 连接已断，不写响应
					if e, ok := rec.(error); ok {
						_ = c.Error(e)
					}
					c.Abort()
					return
				}

				fields := []zap.Field{
					zap.Any("error", rec),
					zap.String("request", reqDump),
				}
				if stack {
					fields = append(fields, zap.String("stack", string(debug.Stack())))
				}

				lg.Error(ctx, "[Recovery from panic]", fields...)
				c.AbortWithStatus(http.StatusInternalServerError)
			}
		}()

		c.Next()
	}
}

// safeRequestDump 输出“可排障但默认不泄露敏感信息”的请求摘要
func safeRequestDump(r *http.Request) string {
	if r == nil {
		return ""
	}

	var b strings.Builder
	b.WriteString(r.Method)
	b.WriteString(" ")
	b.WriteString(r.URL.RequestURI())
	b.WriteString(" ")
	b.WriteString(r.Proto)
	b.WriteString("\n")

	for k, vv := range r.Header {
		lk := strings.ToLower(k)
		switch lk {
		case "authorization", "cookie", "set-cookie", "x-api-key", "x-auth-token":
			b.WriteString(k)
			b.WriteString(": ")
			b.WriteString("[REDACTED]")
			b.WriteString("\n")
			continue
		}
		b.WriteString(k)
		b.WriteString(": ")
		b.WriteString(strings.Join(vv, ","))
		b.WriteString("\n")
	}

	return b.String()
}

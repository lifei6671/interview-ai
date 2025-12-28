package server

import (
	"crypto/rand"
	"encoding/hex"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/lifei6671/logit"
	"go.uber.org/zap"
)

// ContextMetaOptions 可选配置
type ContextMetaOptions struct {
	TraceIDHeaders      []string // 从哪些 header 读取 trace id（按优先级）
	ResponseTraceHeader string   // 回写到响应头的 header 名；空则不回写
}

func DefaultContextMetaOptions() ContextMetaOptions {
	return ContextMetaOptions{
		TraceIDHeaders:      []string{"X-Trace-Id", "X-Request-Id", "Traceparent"},
		ResponseTraceHeader: "X-Trace-Id",
	}
}

// GinWithContextMeta 在 Request.Context 中初始化 logit 容器，并预埋 HTTP 元数据
func GinWithContextMeta(opt ContextMetaOptions) gin.HandlerFunc {
	if len(opt.TraceIDHeaders) == 0 {
		opt.TraceIDHeaders = DefaultContextMetaOptions().TraceIDHeaders
	}

	return func(c *gin.Context) {
		parent := c.Request.Context()

		// 1) 初始化容器：每个请求一份全新容器（更安全）
		ctx := logit.NewContext(parent)

		// 2) trace_id：优先取 header，否则生成
		traceID := extractTraceID(c.Request, opt.TraceIDHeaders)
		if traceID == "" {
			traceID = genTraceID32Hex()
		}

		// 3) 写入元数据（作为 MetaFields：全局自动附带）
		logit.AddMetaFields(ctx,
			zap.String("trace_id", traceID),
			zap.String("user_ip", c.ClientIP()),
			zap.String("path", c.Request.URL.Path),
			zap.String("user_agent", c.Request.UserAgent()),
			zap.String("method", c.Request.Method),
		)

		// 4) 写回 request context
		c.Request = c.Request.WithContext(ctx)

		// 5) 回写响应头，便于排障与链路对齐
		if opt.ResponseTraceHeader != "" {
			c.Writer.Header().Set(opt.ResponseTraceHeader, traceID)
		}

		c.Next()
	}
}

func extractTraceID(r *http.Request, headers []string) string {
	for _, h := range headers {
		v := strings.TrimSpace(r.Header.Get(h))
		if v == "" {
			continue
		}
		// W3C traceparent：version-traceid-spanid-flags
		if strings.EqualFold(h, "Traceparent") {
			if tid := parseTraceParentTraceID(v); tid != "" {
				return tid
			}
		}
		return v
	}
	return ""
}

func parseTraceParentTraceID(tp string) string {
	parts := strings.Split(tp, "-")
	if len(parts) < 4 {
		return ""
	}
	traceID := parts[1]
	if len(traceID) != 32 {
		return ""
	}
	// 简单 hex 校验（可选）
	for _, ch := range traceID {
		if !((ch >= '0' && ch <= '9') || (ch >= 'a' && ch <= 'f') || (ch >= 'A' && ch <= 'F')) {
			return ""
		}
	}
	return strings.ToLower(traceID)
}

func genTraceID32Hex() string {
	var b [16]byte
	_, _ = rand.Read(b[:])
	return hex.EncodeToString(b[:]) // 32 hex chars
}

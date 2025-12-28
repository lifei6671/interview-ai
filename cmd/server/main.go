package main

import (
	"context"
	"errors"
	"flag"
	"log"
	"net"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/lifei6671/interview-ai/actions"
	"github.com/lifei6671/interview-ai/boot"
	"github.com/lifei6671/interview-ai/server"
	"github.com/lifei6671/logit"
)

var configFile = flag.String("config", "conf/app.toml", "path to config file")

func main() {
	flag.Parse()

	rootCtx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
	defer stop()

	appConfig, err := boot.MustLoadServerConfig(*configFile)
	if err != nil {
		log.Println("Failed to load server config:", err)
		os.Exit(1)
	}
	log.Printf("App listen %s", appConfig.Listen)
	log.Printf("App run mode:%s", appConfig.RunMode)
	log.Printf("App root dir:%s", appConfig.RootDir)
	log.Printf("App conf dir:%s", appConfig.ConfDir)
	log.Printf("App log dir:%s", appConfig.LogDir)

	logger := logit.New(logit.Config{ToStdout: true})

	l, err := net.Listen("tcp", appConfig.Listen)
	if err != nil {
		log.Println("Failed to listen:", err)
		os.Exit(1)
	}

	ser := server.New(rootCtx, "", server.WithLogitLogger(logger))

	actions.HttpRouter(ser)

	// Serve 放到 goroutine，主 goroutine 负责 shutdown
	errCh := make(chan error, 1)
	go func() {
		log.Printf("Server starting on %s", appConfig.Listen)
		errCh <- ser.Serve(l)
	}()

	select {
	case <-rootCtx.Done():
		// 收到退出信号
		log.Println("Shutdown signal received")
	case err := <-errCh:
		// Serve 提前返回（启动失败/运行异常）
		if err != nil && !errors.Is(err, http.ErrServerClosed) {
			log.Println("Server stopped unexpectedly:", err)
			os.Exit(1)
		}
		return
	}

	// 优雅退出：给一个超时窗口
	shutdownCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	if err := ser.Shutdown(shutdownCtx); err != nil {
		log.Printf("Graceful shutdown failed:%v", err)
		os.Exit(1)
	}

	// 等 Serve 返回，避免主进程提前退出
	serErr := <-errCh
	if err != nil && !errors.Is(serErr, http.ErrServerClosed) {
		log.Println("Server stopped with error:", serErr)
		os.Exit(1)
	}

	log.Println("Server exited gracefully")
}

func init() {
	log.SetFlags(log.LstdFlags | log.Lshortfile)
}

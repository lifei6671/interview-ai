package routes

import (
	"github.com/gin-gonic/gin"
)

type Route struct {
	Method      string
	Path        string
	Middlewares []gin.HandlerFunc
	Handler     gin.HandlerFunc
}

// Register 注册路由
func Register(r gin.IRoutes, routes ...Route) {
	for _, rt := range routes {
		hs := append([]gin.HandlerFunc{}, rt.Middlewares...)
		hs = append(hs, rt.Handler)
		r.Handle(rt.Method, rt.Path, hs...)
	}
}

// HandleFunc 创建路由
func HandleFunc(method, path string, handler gin.HandlerFunc, middlewares ...gin.HandlerFunc) Route {
	return Route{
		Method:      method,
		Path:        path,
		Handler:     handler,
		Middlewares: middlewares,
	}
}

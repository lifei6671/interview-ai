package actions

import (
	"github.com/lifei6671/interview-ai/actions/health"
	"github.com/lifei6671/interview-ai/routes"
	"github.com/lifei6671/interview-ai/server"
)

// HttpRouter 注册 HTTP 路由
func HttpRouter(ser server.Server) {
	routes.Register(ser.Router(), health.Routers()...)
}

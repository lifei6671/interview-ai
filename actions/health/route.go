package health

import (
	"net/http"

	"github.com/lifei6671/interview-ai/routes"
)

// Routers 路由
func Routers() []routes.Route {
	return []routes.Route{
		routes.HandleFunc(http.MethodGet, "/health", Health),
	}
}

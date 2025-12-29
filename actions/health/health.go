package health

import (
	"github.com/gin-gonic/gin"
	"github.com/lifei6671/logit"
)

func Health(c *gin.Context) {

	logit.DefaultLogger.Error(c, "health check", logit.Any("errmsg", "test"))
	c.JSON(200, gin.H{
		"message": "success",
	})
}

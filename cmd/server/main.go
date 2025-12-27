package main

import (
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

// Greeting model for Gorm verification
type Greeting struct {
	gorm.Model
	Message string
}

func main() {
	// Database Connection
	// Note: using localhost because we are running outside the container, connecting to exposed port
	dsn := "host=localhost user=admin password=admin123 dbname=jd_interview port=5432 sslmode=disable"
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Printf("Warning: failed to connect database: %v. Database features will be disabled.", err)
	} else {
		// Migrate the schema
		if err := db.AutoMigrate(&Greeting{}); err != nil {
			log.Printf("Warning: failed to migrate database: %v", err)
		} else {
			// Create a default greeting if not exists (just for demo)
			var count int64
			db.Model(&Greeting{}).Count(&count)
			if count == 0 {
				db.Create(&Greeting{Message: "Hello from Gorm!"})
			}
		}
	}

	// Gin Router
	r := gin.Default()

	// Hello World Endpoint
	r.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "Hello World from Gin!",
		})
	})

	// Endpoint to get greeting from DB
	r.GET("/db-hello", func(c *gin.Context) {
		if db == nil || db.Error != nil {
			c.JSON(http.StatusServiceUnavailable, gin.H{"error": "Database not connected"})
			return
		}
		var greeting Greeting
		if result := db.First(&greeting); result.Error != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": result.Error.Error()})
			return
		}
		c.JSON(http.StatusOK, gin.H{
			"message": greeting.Message,
			"source":  "PostgreSQL",
		})
	})

	log.Println("Server starting on :8080")
	if err := r.Run(":8080"); err != nil {
		log.Fatal("Server failed to start: ", err)
	}
}

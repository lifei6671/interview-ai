package boot

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/lifei6671/go-config"
	"github.com/lifei6671/go-config/decoder"
)

const (
	// RunModeDev 开发环境
	RunModeDev = "dev"
	// RunModeTest 测试环境
	RunModeTest = "test"
	// RunModeProd 生成环境
	RunModeProd = "prod"
)

// AppConfig 服务配置
type AppConfig struct {
	// 运行模式
	RunMode string
	// 服务监听地址
	Addr string
	// 读超时
	ReadTimeout int
	// 写超时
	WriteTimeout int

	// 应用根目录,若为空则自动推断
	RootDir string

	// 日志目录,默认为 RootDir + "/log/"
	LogDir string

	// 配置文件目录,默认为 RootDir + "/conf/"
	ConfDir string
}

// MustLoadServerConfig 加载服务配置
func MustLoadServerConfig(filename string) (*AppConfig, error) {
	// 验证文件路径，防止路径遍历攻击
	if !filepath.IsAbs(filename) {
		return nil, fmt.Errorf("filename must be an absolute path: %s", filename)
	}

	// 获取当前工作目录，限制配置文件必须在应用目录内
	execDir, err := filepath.Abs(filepath.Dir(os.Args[0]))
	if err != nil {
		return nil, fmt.Errorf("failed to get executable directory: %w", err)
	}

	// 确保配置文件在执行目录下，防止路径遍历
	absPath, err := filepath.Abs(filename)
	if err != nil {
		return nil, fmt.Errorf("failed to get absolute path for %s: %w", filename, err)
	}

	relPath, err := filepath.Rel(execDir, absPath)
	if err != nil {
		return nil, fmt.Errorf("failed to get relative path: %w", err)
	}

	// 检查相对路径是否包含上级目录引用
	if strings.HasPrefix(relPath, ".."+string(filepath.Separator)) || relPath == ".." {
		return nil, fmt.Errorf("config file path is outside the application directory: %s", filename)
	}

	cfg := config.NewDefaultConfig(
		config.WithDecoder(decoder.TOMLDecoder{}),
	)
	err = cfg.Load(config.NewFileSource(filename))
	if err != nil {
		return nil, fmt.Errorf("load config fail from %s: %w", filename, err)
	}
	var c AppConfig
	err = cfg.Unmarshal(&c)
	if err != nil {
		return nil, fmt.Errorf("unmarshal config fail from %s: %w", filename, err)
	}

	if c.RootDir == "" {
		c.RootDir = execDir
	}
	if c.LogDir == "" {
		c.LogDir = filepath.Join(c.RootDir, "log")
	}
	if c.ConfDir == "" {
		c.ConfDir = filepath.Join(c.RootDir, "conf")
	}
	return &c, nil
}

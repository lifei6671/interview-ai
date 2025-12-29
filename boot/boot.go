package boot

import (
	"fmt"
	"log"
	"path/filepath"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/lifei6671/go-config"
	"github.com/lifei6671/go-config/decoder"
	"github.com/lifei6671/interview-ai/boot/configloc"
)

const (
	// RunModeDebug 开发环境
	RunModeDebug = gin.DebugMode
	// RunModeTest 测试环境
	RunModeTest = gin.TestMode
	// RunModeRelease 生成环境
	RunModeRelease = gin.ReleaseMode
)

// AppConfig 服务配置
type AppConfig struct {
	AppName string `json:"AppName,omitempty" yaml:"AppName" toml:"AppName"`
	// 运行模式
	RunMode string `json:"RunMode,omitempty" yaml:"RunMode" toml:"RunMode"`
	// 服务监听地址
	Listen string `json:"Listen,omitempty" yaml:"Listen" toml:"Listen"`
	// 读超时
	ReadTimeout int `json:"ReadTimeout,omitempty" yaml:"ReadTimeout" toml:"ReadTimeout"`
	// 写超时
	WriteTimeout int `json:"WriteTimeout,omitempty" yaml:"WriteTimeout" toml:"WriteTimeout"`

	// 应用根目录,若为空则自动推断
	RootDir string `json:"RootDir,omitempty" yaml:"RootDir" toml:"RootDir"`

	// 日志目录,默认为 RootDir + "/log/"
	LogDir string `json:"LogDir,omitempty" yaml:"LogDir" toml:"LogDir"`

	// 配置文件目录,默认为 RootDir + "/conf/"
	ConfDir string `json:"ConfDir,omitempty" yaml:"ConfDir" toml:"ConfDir"`

	LogConfig LogConfig `json:"LogConfig,omitempty" yaml:"LogConfig" toml:"LogConfig"`
}

type LogConfig struct {
	// 日志文件名
	Filename string `json:"Filename,omitempty" yaml:"Filename" toml:"Filename"`
	// 日志分发规则名称
	RuleName string `json:"RuleName,omitempty" yaml:"RuleName" toml:"RuleName"`
	// 日志刷新间隔
	FlushDuration int `json:"FlushDuration,omitempty" yaml:"FlushDuration" toml:"FlushDuration"`
	// 日志检查间隔，定时检查日志文件是否被删除
	CheckDuration int `json:"CheckDuration,omitempty" yaml:"CheckDuration" toml:"CheckDuration"`
	// 保存的最大文件数量，多于该数量则清理，如果为0则忽略
	MaxFileNum int
	// 日志缓冲区大小
	BufferSize int
	// 日志分发规则
	DispatchRule []LogDispatchRule `json:"DispatchRule,omitempty" yaml:"DispatchRule" toml:"DispatchRule"`
}

type LogDispatchRule struct {
	// 文件后缀
	FileSuffix string `json:"FileSuffix,omitempty" yaml:"FileSuffix" toml:"FileSuffix"`
	// 日志级别
	Levels []string `json:"levels,omitempty" yaml:"Levels" toml:"Levels"`

	// 日志编码器名称: json/console
	Encoder string `json:"Encoder,omitempty" yaml:"Encoder" toml:"Encoder"`
}

// MustLoadServerConfig 加载服务配置
func MustLoadServerConfig(filename string) (*AppConfig, error) {
	// 获取当前工作目录，限制配置文件必须在应用目录内
	execDir, err := DetectAppDir(filename)
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
		config.WithDecoder(decoder.YAMLDecoder{}),
		config.WithVariableExpander(config.DefaultVariableExpander{}),
	)
	cfg.EnableEnvExpand()

	err = cfg.Load(
		config.NewFileSource(filename),
	)
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
	if c.AppName == "" {
		c.AppName = "interview-ai"
	}
	Print(c)
	return &c, nil
}

// DetectAppDir 检测应用目录
func DetectAppDir(cfgArg string) (string, error) {

	res, err := configloc.Resolve(configloc.Options{
		AppName:          "interview-ai",
		ConfigArg:        cfgArg,
		AllowDevRootScan: true,
	})
	if err != nil {
		return "", err
	}
	dir, err := filepath.Abs(filepath.Join(filepath.Dir(res.Path), "../"))
	if err != nil {
		return "", err
	}
	return dir, nil
}

// Print 打印服务配置
func Print(e AppConfig) {
	type data struct {
		Key   string
		Value string
	}
	kvs := []data{
		{
			Key:   "AppName",
			Value: e.AppName,
		},
		{
			Key:   "Listen",
			Value: e.Listen,
		},
		{
			Key:   "RunMode",
			Value: e.RunMode,
		},
		{
			Key:   "RootDir",
			Value: e.RootDir,
		},
		{
			Key:   "ConfDir",
			Value: e.ConfDir,
		},
		{
			Key:   "LogDir",
			Value: e.LogDir,
		},
	}
	bs := &strings.Builder{}
	bs.WriteString("AppConfig:\n")
	for _, kv := range kvs {
		bs.WriteString(fmt.Sprintf("%20s\t%q\n", kv.Key, kv.Value))
	}
	_ = log.Output(2, bs.String())
}

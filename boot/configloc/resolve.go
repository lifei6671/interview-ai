package configloc

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

type Options struct {
	// AppName 用于拼接 /etc/<app>/... 目录
	AppName string

	// ConfigArg 命令行解析出来的 --config 值（外部传进来，避免此包依赖 flag）
	ConfigArg string

	// EnvKey 环境变量名，默认 CONFIG_PATH
	EnvKey string

	// DefaultRelCandidates 相对路径候选（基于 cwd、exeDir、devRoot）
	// 例如：conf/app.toml, config/app.yaml 等
	DefaultRelCandidates []string

	// DevRootMarkers 用于开发态向上探测根目录的 marker
	// 例如：go.mod, .git, conf/app.toml
	DevRootMarkers []string

	// MaxParentLevels 向上查找的最大层级（防止极端情况）
	MaxParentLevels int

	// AllowDevRootScan 是否允许向上探测（建议默认 true）
	AllowDevRootScan bool

	// ExtraAbsCandidates 额外绝对路径候选（例如 /etc/app/config.yaml）
	ExtraAbsCandidates []string
}

type Result struct {
	Path   string // 最终配置文件路径（绝对路径）
	Source string // 命中来源：flag/env/cwd/exe/devroot/etc...
}

var ErrConfigNotFound = errors.New("config not found")

func Resolve(opt Options) (Result, error) {
	if opt.EnvKey == "" {
		opt.EnvKey = "CONFIG_PATH"
	}
	if opt.MaxParentLevels <= 0 {
		opt.MaxParentLevels = 30
	}
	if opt.DefaultRelCandidates == nil {
		opt.DefaultRelCandidates = []string{
			filepath.Join("conf", "app.toml"),
			filepath.Join("conf", "app.yaml"),
			filepath.Join("conf", "app.yml"),
			filepath.Join("config", "app.toml"),
			filepath.Join("config", "app.yaml"),
			filepath.Join("config", "app.yml"),
		}
	}
	if opt.DevRootMarkers == nil {
		opt.DevRootMarkers = []string{
			"go.mod",
			".git",
			filepath.Join("conf", "app.toml"),
		}
	}
	if opt.AllowDevRootScan == false {
		// 保持用户显式配置
	}

	// 1) flag: --config
	if p := strings.TrimSpace(opt.ConfigArg); p != "" {
		if res, ok := verifyPath(p, "flag"); ok {
			return res, nil
		}
		return Result{}, fmt.Errorf("config from flag not found: %s", p)
	}

	// 2) env: CONFIG_PATH
	if p := strings.TrimSpace(os.Getenv(opt.EnvKey)); p != "" {
		if res, ok := verifyPath(p, "env"); ok {
			return res, nil
		}
		return Result{}, fmt.Errorf("config from env %s not found: %s", opt.EnvKey, p)
	}

	// 基础目录准备
	wd, _ := os.Getwd()
	exeDir, _ := executableDir()

	// 3) K8s/Docker 常见挂载点：/config、/etc/<app>、/etc/config 等
	absCandidates := make([]string, 0, 16)
	absCandidates = append(absCandidates, opt.ExtraAbsCandidates...)

	// /config (很多人会 mount 到 /config)
	absCandidates = append(absCandidates,
		"/config/app.toml",
		"/config/app.yaml",
		"/config/app.yml",
	)

	// /etc/config (K8s ConfigMap 常见)
	absCandidates = append(absCandidates,
		"/etc/config/app.toml",
		"/etc/config/app.yaml",
		"/etc/config/app.yml",
	)

	// /etc/<app>/...
	if opt.AppName != "" {
		absCandidates = append(absCandidates,
			filepath.Join("/etc", opt.AppName, "app.toml"),
			filepath.Join("/etc", opt.AppName, "app.yaml"),
			filepath.Join("/etc", opt.AppName, "app.yml"),
			filepath.Join("/etc", opt.AppName, "config.toml"),
			filepath.Join("/etc", opt.AppName, "config.yaml"),
			filepath.Join("/etc", opt.AppName, "config.yml"),
		)
	}

	for _, p := range absCandidates {
		if res, ok := verifyPath(p, "abs"); ok {
			return res, nil
		}
	}

	// 4) cwd + 默认相对候选
	if wd != "" {
		for _, rel := range opt.DefaultRelCandidates {
			p := filepath.Join(wd, rel)
			if res, ok := verifyPath(p, "cwd"); ok {
				return res, nil
			}
		}
	}

	// 5) exeDir + 默认相对候选（生产二进制旁带 conf/config）
	if exeDir != "" {
		for _, rel := range opt.DefaultRelCandidates {
			p := filepath.Join(exeDir, rel)
			if res, ok := verifyPath(p, "exe"); ok {
				return res, nil
			}
		}
	}

	// 6) 开发态向上探测根目录，再从根目录拼默认相对候选
	if opt.AllowDevRootScan && wd != "" {
		if root, err := findDevRoot(wd, opt.DevRootMarkers, opt.MaxParentLevels); err == nil && root != "" {
			for _, rel := range opt.DefaultRelCandidates {
				p := filepath.Join(root, rel)
				if res, ok := verifyPath(p, "devroot"); ok {
					return res, nil
				}
			}
		}
	}

	return Result{}, fmt.Errorf("%w: tried flag/env/abs/cwd/exe/devroot", ErrConfigNotFound)
}

func verifyPath(p string, source string) (Result, bool) {
	// 支持相对路径（相对路径以 cwd 解析）
	if !filepath.IsAbs(p) {
		if wd, err := os.Getwd(); err == nil && wd != "" {
			p = filepath.Join(wd, p)
		}
	}
	p = filepath.Clean(p)

	st, err := os.Stat(p)
	if err != nil {
		return Result{}, false
	}
	if st.IsDir() {
		return Result{}, false
	}
	return Result{Path: p, Source: source}, true
}

func executableDir() (string, error) {
	exe, err := os.Executable()
	if err != nil {
		return "", err
	}
	exe, err = filepath.EvalSymlinks(exe)
	if err != nil {
		return "", err
	}
	return filepath.Dir(exe), nil
}

func findDevRoot(baseDir string, markers []string, maxDepth int) (string, error) {
	cur := baseDir
	for i := 0; i < maxDepth; i++ {
		if dirHasAny(cur, markers) {
			return cur, nil
		}
		parent := filepath.Dir(cur)
		if parent == cur {
			break
		}
		cur = parent
	}
	return "", ErrConfigNotFound
}

func dirHasAny(dir string, markers []string) bool {
	for _, m := range markers {
		p := filepath.Join(dir, m)
		_, err := os.Stat(p)
		if err == nil {
			return true
		}
		if !os.IsNotExist(err) {
			// 权限/IO 错误不当作命中，避免误判
			continue
		}
	}
	return false
}

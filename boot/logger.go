package boot

import (
	"log"
	"time"

	"github.com/lifei6671/logit"
	"go.uber.org/zap/zapcore"
)

// MustLogger 创建日志组件
func MustLogger(appConfig *AppConfig) (*logit.Logger, logit.CloseFunc, error) {
	var dispatchRules []logit.ZapDispatch

	for _, rule := range appConfig.LogConfig.DispatchRule {
		encoderBuilder := logit.NewJSONEncoder()

		switch rule.Encoder {
		case "console":
			encoderBuilder = logit.NewConsoleEncoder()
		default:
		}

		dispatchRules = append(dispatchRules, logit.ZapDispatch{
			EncoderBuilder: encoderBuilder,
			FileSuffix:     rule.FileSuffix,
			Levels: func() []zapcore.Level {
				var levels []zapcore.Level
				for _, level := range rule.Levels {
					levels = append(levels, logit.ParseLevel(level))
				}
				return levels
			}(),
		})
	}
	logger, c, err := logit.NewWithDispatch(
		appConfig.LogConfig.RuleName,
		appConfig.LogConfig.Filename,
		dispatchRules,
		logit.DefaultWriterBuild,
		logit.NewJSONEncoder(),
		logit.WithCheckDuration(time.Second*time.Duration(appConfig.LogConfig.CheckDuration)),
		logit.WithMaxFileNum(appConfig.LogConfig.MaxFileNum),
		logit.WithFlushDuration(time.Second*time.Duration(appConfig.LogConfig.FlushDuration)),
		logit.WithBufferSize(appConfig.LogConfig.BufferSize),
		logit.WithOnErr(func(err error) {
			log.Println("Failed to create logger:", err)
		}),
	)
	if err != nil {
		return nil, nil, err
	}
	return logger, c, nil
}

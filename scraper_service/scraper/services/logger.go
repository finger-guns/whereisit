package services


import (
	z "go.uber.org/zap"
)

func Logger() (*z.Logger, error) {
	logger, err := z.NewProduction()
	logger.Sugar()
	if err != nil {
		return nil, err
	}
	return logger, nil
}


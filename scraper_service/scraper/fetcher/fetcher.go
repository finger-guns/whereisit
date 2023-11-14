package fetcher

import (
	"io"
	"net/http"

	"go.uber.org/zap"
)

type HTTPFetcher struct {
	Client *http.Client
	Logger *zap.Logger
}

type Fetcher interface {
	Fetch(url string) (*http.Response, error)
}

func (fetcher HTTPFetcher) Fetch(url string) (*http.Response, error) {
	request, err := http.NewRequest(http.MethodGet, url, nil)

	if err != nil {
		fetcher.Logger.Error("Error creating request", zap.Error(err))
		return nil, err
	}

	response, err := fetcher.Client.Do(request)

	if err != nil {
		fetcher.Logger.Error("Error creating request", zap.Error(err))
		return nil, err
	}

	return response, nil
}

func ToByte(response *http.Response) ([]byte, error) {
	defer response.Body.Close()

	body, err := io.ReadAll(response.Body)

	if err != nil {
		return nil, err
	}

	return body, nil
}

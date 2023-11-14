package fetcher


import (
	"bytes"
	"io"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestHTTPFetcher_Fetch(t *testing.T) {
	mockServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("mocked response"))
	}))
	defer mockServer.Close()

	fetcher := HTTPFetcher{Client: http.DefaultClient}

	resp, err := fetcher.Fetch(mockServer.URL)
	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}
	defer resp.Body.Close()

	body, err := ToByte(resp)
	if err != nil {
		t.Fatalf("Expected no error reading body, got %v", err)
	}

	expectedBody := "mocked response"
	if string(body) != expectedBody {
		t.Fatalf("Expected %s, got %s", expectedBody, body)
	}
}

func TestToByte(t *testing.T) {
	mockResponse := &http.Response{
		Body: io.NopCloser(bytes.NewBufferString("mocked response")),
	}

	body, err := ToByte(mockResponse)
	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}

	expectedBody := "mocked response"
	if string(body) != expectedBody {
		t.Fatalf("Expected %s, got %s", expectedBody, body)
	}
}

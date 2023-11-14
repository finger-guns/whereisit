package main

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"regexp"
	"strings"

	"github.com/jackc/pgx/v5/pgxpool"
	z "go.uber.org/zap"
	f "whereisit.xyz/scraper/fetcher"
	s "whereisit.xyz/scraper/services"
	u "whereisit.xyz/scraper/utils"
)

type MessageRequest struct {
	JobID string `json:"job_id"`
	Title string `json:"title"`
	IsMovie bool   `json:"is_movie"`
	IsTv    bool   `json:"is_tv"`
}

type FormatterRequest struct {
	JobID string `json:"job_id"`
	ScraperId string `json:"scraper_id"`
	HTMLBytes []byte `json:"html_bytes"`
}

const (
	REDIS_CHANNEL = "to-scrape"
)

func toSnakeCase(s string) string {
	s = strings.ToLower(s)
	re := regexp.MustCompile(`\s+`)
	s = re.ReplaceAllString(s, "_")
	return s
}

func formatUrl(message MessageRequest) string {
	var url string

	title := toSnakeCase(message.Title)
	
	if message.IsMovie {
		url = fmt.Sprintf("https://www.rottentomatoes.com/m/%s", title)
	}
	if message.IsTv {
		url = fmt.Sprintf("https://www.rottentomatoes.com/tv/%s", title)
	}

	return url
}

func setupPool(config u.Config) (*pgxpool.Pool, error) {
	pool, err := pgxpool.New(
		context.Background(),
		fmt.Sprintf("postgres://%s:%s@%s:%s/%s",
			config.PostgresUser,
			config.PostgresPassword,
			config.PostgresHost,
			config.PostgresPort,
			config.PostgresDatabase),
	)

	if err != nil {
		return nil, err
	}

	return pool, nil
}

func startSubscriber(
	messageQueue s.MessageQueueService,
	db *s.DatabaseService,
	fetcher *f.HTTPFetcher,
) {
	subscriber, err := messageQueue.Subscribe(context.Background(), REDIS_CHANNEL)
	if err != nil {
		messageQueue.Logger.Error("Error subscribing channel", z.String("channel", REDIS_CHANNEL))
		return
	}

	defer subscriber.Close()

	var payload MessageRequest

	for {
		message, err := subscriber.ReceiveMessage(context.Background())
		messageQueue.Logger.Info("Received message", z.String("channel", message.Payload))
		if err != nil {
			messageQueue.Logger.Error("Error receiving message", z.String("channel", REDIS_CHANNEL))
			continue
		}

		if err = json.Unmarshal([]byte(message.Payload), &payload); err != nil {
			messageQueue.Logger.Error("Error unmarshalling message", z.String("channel", REDIS_CHANNEL))
			continue
		}

		url := formatUrl(payload)

		messageQueue.Logger.Info(
			"PAYLOAD",
			z.String("url", url),
			z.String("jobId", payload.JobID),
			z.String("title", payload.Title),
			z.Bool("movie", payload.IsMovie),
			z.Bool("tv", payload.IsTv),
		)
		
		response, err := fetcher.Fetch(url)
		if err != nil {
			fmt.Println(err)
			continue
		}

		byteData, err := f.ToByte(response)
		if err != nil {
			fetcher.Logger.Error("Error converting response to byte", z.Error(err))
			response.Body.Close()
			continue
		}


		movieId, err := db.Insert(
			context.Background(),
			payload.JobID,
			payload.Title,
			url,
			byteData,
		)
		if err != nil {
			db.Logger.Error("Error inserting into database", z.Error(err))
			return
		}

		messageData := FormatterRequest{
			JobID: payload.JobID,
			ScraperId:  movieId,
			HTMLBytes: byteData,
    }

		formatterMessage, err := json.Marshal(messageData)

		if err != nil {
			messageQueue.Logger.Error(
				"Error marshalling message",
				z.String("channel", REDIS_CHANNEL),
			)
			continue
		}

		messageQueue.Publish(
			context.Background(),
			"to-format",
			formatterMessage,
		)
	}
}

func main() {
	logger, err := s.Logger()

	if err != nil {
		logger.Fatal("Failed to initialize logger", z.Error(err))
	}

	config := u.LoadConfig()

	client := s.Client(fmt.Sprintf("%s:%s", config.RedisHost, config.RedisPort), 0)

	dbPool, err := setupPool(config)

	if err != nil {
		logger.Fatal("Failed to connect to database", z.Error(err))
	}

	defer dbPool.Close()

	database := s.DatabaseService{
		Pool:   dbPool,
		Logger: *logger,
	}

	messageQueue := s.MessageQueueService{
		Client: client,
		Logger: *logger,
	}

	fetcher := f.HTTPFetcher{
		Client: &http.Client{},
		Logger: logger,
	}

	go startSubscriber(messageQueue, &database, &fetcher)

	select {}

}

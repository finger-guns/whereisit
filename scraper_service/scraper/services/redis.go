package services

import (
	"context"

	r "github.com/redis/go-redis/v9"
	z "go.uber.org/zap"
)

type MessageQueue interface {
	Publish(ctx context.Context, channel string, message interface{}) error
	Subscribe(ctx context.Context, channel string) (*r.PubSub, error)
}

type MessageQueueService struct {
	Client *r.Client
	Logger z.Logger
}

func Client(addr string, db int) *r.Client {
	return r.NewClient(&r.Options{
		Addr: addr,
		DB:   db,
	})
}

func (mq *MessageQueueService) Publish(ctx context.Context, channel string, message interface{}) error {
	err := mq.Client.Publish(ctx, channel, message).Err()
	if err != nil {
		mq.Logger.Error("Error publishing message", z.Error(err))
		return err
	}
	mq.Logger.Info("Message published", z.String("channel", channel))
	return nil
}

func (mq *MessageQueueService) Subscribe(ctx context.Context, channel string) (*r.PubSub, error) {
	pubsub := mq.Client.Subscribe(ctx, channel)
	_, err := pubsub.Receive(ctx)
	if err != nil {
		mq.Logger.Error("Error subscribing channel", z.String("channel", channel))
		return nil, err
	}
	mq.Logger.Info("Subscribed channel", z.String("channel", channel))
	return pubsub, nil
}

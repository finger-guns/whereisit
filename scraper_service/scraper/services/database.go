package services

import (
	"context"

	"github.com/jackc/pgx/v5/pgxpool"
	"go.uber.org/zap"
)

type Database interface {
	Insert(context.Context, string, string) error
}

type DatabaseService struct {
	Pool   *pgxpool.Pool
	Logger zap.Logger
}

func (d DatabaseService) Insert(
	ctx context.Context,
	jobID string,
	title string,
	url string,
	byte []byte,
) (string, error) {
	var insertedID string
	err := d.Pool.QueryRow(
		ctx,
		`INSERT INTO "movie_scraper" (job_id, title, url, bytes) VALUES ($1, $2, $3, $4) RETURNING id`,
		jobID,
		title,
		url,
		byte,
	).Scan(&insertedID)

	if err != nil {
		d.Logger.Error(
			"Error inserting into database",
			zap.String("jobId", jobID),
			zap.String("title", title),
			zap.String("url", url),
		)
		return "", err
	}

	return insertedID, nil
}

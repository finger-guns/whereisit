CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS "movie_format"(
  "id" UUID DEFAULT uuid_generate_v4(),
  "job_id" UUID,
  "title" TEXT,
  "synopsis" TEXT,
  "info" TEXT[] NOT NULL DEFAULT '{}',
  "where_to_watch" TEXT[] NOT NULL DEFAULT '{}',
  "movie_scraper_id" UUID not null,
  "created_at" TIMESTAMP default now(),
  "updated_at" TIMESTAMP default now()
);

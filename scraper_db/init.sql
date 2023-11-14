CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS "movie_scraper"(
  "id" UUID DEFAULT uuid_generate_v4(),
  "job_id" UUID,
  "title" VARCHAR(255) not null,
  "url" TEXT not null,
  "bytes" BYTEA,
  "created_at" TIMESTAMP default now(),
  "updated_at" TIMESTAMP default now()
);

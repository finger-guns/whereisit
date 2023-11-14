from asyncio import run
from json import dumps
from base64 import b64encode
from typing import Any

from utils.config import Config, init_logging
from services.redis import connection, pubsub, subscribe
from services.database import MovieDatabase
from operations.process import (
    prepare_message_info,
    process_message_raw,
    message_to_be_sent,
)
from logging import error, info

# Configuration setup
DATABASE = MovieDatabase(
    host=Config.POSTGRES_HOST,
    port=Config.POSTGRES_PORT,
    user=Config.POSTGRES_USER,
    password=Config.POSTGRES_PASSWORD,
    database=Config.POSTGRES_DATABASE,
)
init_logging()


async def database_insert(
    database: MovieDatabase, message: dict, job_id: str, scraper_id: str
) -> Any | None:
    params = (
        job_id,
        scraper_id,
        str(message["title"]),
        str(message["synopsis"]),
        [str(element) for element in message["where_to_watch"]],
        [str(element) for element in message["info_items"]],
    )
    return await database.insert_into(params)


async def main():
    info("Service Starting")
    redis_client = await connection(
        Config.REDIS_HOST,
        Config.REDIS_PORT,
    )
    pubsub_client = await pubsub(redis_client)
    subscriber = await subscribe(pubsub_client)
    db_connection = await DATABASE.connect()

    async for job_request in subscriber.listen():
        if job_request["type"] == "message":
            info("Message received")
            message_info = prepare_message_info(job_request)
            if not message_info:
                error("Message preparation failed")
                continue

            movie_raw_dict = process_message_raw(message_info)
            if not movie_raw_dict:
                error("Message processing failed")
                continue

            database_result = await database_insert(
                db_connection,
                movie_raw_dict["movie_html_elements"],
                movie_raw_dict["job_id"],
                movie_raw_dict["scraper_id"],
            )
            if not database_result:
                error("Database insertion failed")
                continue

            message = dumps(
                message_to_be_sent(
                    message=movie_raw_dict["movie_html_elements"],
                    formatter_database_id=str(database_result),
                    scraper_id=movie_raw_dict["scraper_id"],
                    job_id=movie_raw_dict["job_id"],
                )
            )
            await redis_client.set(
                name=f"job_request:{movie_raw_dict['job_id']}",
                value=b64encode(message.encode("utf-8")),
            )
            info("Message published")


if __name__ == "__main__":
    run(main())

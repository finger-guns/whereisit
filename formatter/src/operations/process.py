from base64 import b64decode
from typing import Any
from json import loads

from bs4 import BeautifulSoup, Tag

from operations.format import extract_info_items_values, extract_movie_info


def prepare_message_info(
    message: dict[str, str | bytes] | Any,
) -> dict[str, str]:
    data = loads(message['data'].decode('utf-8'))
    return {
        "job_id": data['job_id'],
        "scraper_id": data['scraper_id'],
        "html": b64decode(data['html_bytes']).decode('utf-8'),
    }


def message_to_be_sent(
    message: dict[str, Tag | list[Tag]],
    formatter_database_id: str,
    scraper_id: str,
    job_id: str,
) -> dict[str, Any]:
    return {
        "job_id": job_id,
        "scraper_id": scraper_id,
        "formater_id": formatter_database_id,
        "processed_movie": {
            "title": str(message['title'].text),
            "synopsis": str(message['synopsis'].text),
            "where_to_watch": [element.get('image') for element in message['where_to_watch']],
            "info_items": extract_info_items_values(message['info_items']),
        }
    }


def process_message_raw(
    message_info: dict[str, str],
) -> dict[str, Any] | None:
    soup = BeautifulSoup(
        message_info["html"],
        features="html.parser",
    )

    movie_information = extract_movie_info(
        soup,
    )
    
    return {
        "job_id": str(message_info["job_id"]),
        "scraper_id": str(message_info["scraper_id"]),
        "formatter_id": None,
        "movie_html_elements": {
            "title": movie_information.title,
            "synopsis": movie_information.synopsis,
            "where_to_watch": movie_information.where_to_watch,
            "info_items": movie_information.info_items,
        }
    }

from typing import NamedTuple
from bs4 import BeautifulSoup, NavigableString, Tag


class MovieInformationRaw(NamedTuple):
    title: NavigableString | Tag
    synopsis: NavigableString | Tag
    info_items: list[Tag]
    where_to_watch: list[Tag]


def find_element_by_data_qa(
    soup: BeautifulSoup,
    tag: str,
    data_qa_value: str,
) -> Tag | NavigableString:
    return soup.find(tag, attrs={"data-qa": data_qa_value}) or Tag(name="")


def find_elements_by_data_qa(
    soup: BeautifulSoup,
    tag: str,
    data_qa_value: str,
) -> list[Tag]:
    return soup.findAll(tag, attrs={"data-qa": data_qa_value})


def extract_where_to_watch(
    soup: BeautifulSoup,
) -> list[Tag]:
    return soup.findAll("where-to-watch-bubble")


def extract_movie_info(
    soup: BeautifulSoup,
) -> MovieInformationRaw:
    return MovieInformationRaw(
        title=find_element_by_data_qa(soup, "h1", "score-panel-title"),
        synopsis=find_element_by_data_qa(soup, "p", "movie-info-synopsis"),
        info_items=find_elements_by_data_qa(soup, "li", "movie-info-item"),
        where_to_watch=extract_where_to_watch(soup),
    )


def extract_info_items_values(
    info_items: list[Tag],
) -> dict[str, str]:
    extracted_info = {}

    for item in info_items: # To be a list chomp later.
        label_element = item.find(attrs={"data-qa": "movie-info-item-label"})
        value_element = item.find(attrs={"data-qa": "movie-info-item-value"})

        label_text = (
            label_element.get_text().rstrip() if label_element else None
        )
        value_text = (
            value_element.get_text().rstrip() if value_element else None
        )

        if label_text is not None:
            extracted_info[label_text] = value_text

    return extracted_info

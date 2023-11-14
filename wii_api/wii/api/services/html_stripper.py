from typing import List
from bs4 import BeautifulSoup



def text_from_html(
    html: str,
) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    return text


def text_from_attribute(
    html: str,
    tag: str,
    attribute: str,
) -> List[str]:
    """
    Return the value for the attribute passed in.
    ie -
    html = "<where-to-watch-bubble image="vudu" slot="bubble" tabindex="-1"></where-to-watch-bubble>"
    tag = "where-to-watch-bubble"
    attribute = "image"
    returns "vudu"
    """
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.find_all(tag, class_=attribute)
    return [element[attribute] for element in elements if element.has_attr('image')]

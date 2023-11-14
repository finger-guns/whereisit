from src.operations.format import info_items, synopsis, where_to_watch, title
from bs4 import BeautifulSoup, Tag


def test_movie_title(soup_matrix: BeautifulSoup) -> None:
    x = title(soup_matrix)
    assert x
    assert x.text == 'The Matrix'


def test_synopsis_getter(soup_matrix: BeautifulSoup) -> None:
    x =  synopsis(soup_matrix)
    assert x
    assert x.text.strip() == '''
    Neo (Keanu Reeves) believes that Morpheus (Laurence Fishburne), an elusive figure considered to be the most dangerous man alive, can answer his question -- What is the Matrix? Neo is contacted by Trinity (Carrie-Anne Moss), a beautiful stranger who leads him into an underworld where he meets Morpheus. They fight a brutal battle for their lives against a cadre of viciously intelligent secret agents. It is a truth that could cost Neo something more precious than his life.
    '''.strip()


def test_info_items(soup_matrix: BeautifulSoup) -> None:
    x =  info_items(soup_matrix)
    assert x
    assert len(x) == 15
    print(x[0].text)
    assert x[0].text.strip() == 'Rating: R (Sci-Fi Violence|Brief Language)'


def test_where_to_watch(soup_matrix: BeautifulSoup) -> None:
    x = where_to_watch(soup_matrix)
    assert x
    assert len(x) == 6
    print(x[0].text)
    assert x[0].text.strip() == 'In Theaters'

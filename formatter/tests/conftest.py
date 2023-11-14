from bs4 import BeautifulSoup
from pytest import fixture
from os.path import dirname, realpath, join


CONFTEST_DIR = dirname(realpath(__file__))
HTML_FILE_PATH = join(CONFTEST_DIR, 'helpers', 'minimatrix.html')


@fixture
def soup_matrix() -> BeautifulSoup:
    with open(HTML_FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    return BeautifulSoup(content, 'html.parser')

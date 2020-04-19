import sys
sys.path.append("..")
sys.path.append("../src")

from src import *


def test_cantar():

    word = "cantar"
    url = f'https://dlc.iec.cat/results.asp?txtEntrada={word}'
    get_webpage(url)
    with open('iec_cantar.txt', 'r') as f:
        soup = bs4.BeautifulSoup(f.read(), 'html.parser')
    definitions = get_definitions(soup)
    assert(len(definitions) == 20)

def test_cantar_examples():

    word = "cantar"
    url = f'https://dlc.iec.cat/results.asp?txtEntrada={word}'
    get_webpage(url)
    with open('iec_cantar.txt', 'r') as f:
        soup = bs4.BeautifulSoup(f.read(), 'html.parser')
    definitions = get_definitions(soup)
    assert(len(list(definitions)) == 20)
import os

from bs4 import BeautifulSoup
import requests

import exceptions

DEBUG = True
if DEBUG and not os.path.exists('../logs'):
    os.makedirs('../logs')


def get_soup(url, word):
    html_get = requests.get(url)
    soup_get = BeautifulSoup(html_get.text, 'html.parser')

    if DEBUG:
        with open(f'../logs/{word}_get.html', 'w') as f:
            f.write(soup_get.prettify())

    definitions_html = soup_get.find(class_="resultDefinition")
    not_found = "No s'ha trobat cap entrada coincident amb els criteris de cerca"
    if (definitions_html.text == not_found):
        raise exceptions.WordNotFoundError(f'{word} not found')

    # Get all the id of the words that are different words (different in length)
    # and the ones that have same accentuation.
    ids = [html['id'] for html in soup_get.find_all(class_='resultAnchor')
           if (len(word) != len(html.text.strip()) or word == html.text.strip())]

    soups = []
    for id_ in ids:
        params = {'id': id_, 'searchParam': word}
        url_post = 'https://dlc.iec.cat/Results/Accepcio'

        html_post = requests.post(url_post, data=params)
        soup_post = BeautifulSoup(html_post.text, 'html.parser')
        if DEBUG:
            with open(f'../logs/{word}{id_}.html', 'w') as f:
                f.write(soup_post.prettify())
        soups.append(soup_post)

    return soups


def scrap_definitions(soups, word, examples=False):
    """
    Given the soup of the IEC webpage of a word it retrieves a list of the definitions.
    If example is true, a list of tupples (definition,example) will be retrieved.
    If a definition has no examples, the value returned is None.
    """
    definitions_list = []
    examples_list = []
    for soup in soups:
        definitions_html = soup.find_all(name='span', class_="\\\"body\\\"")  # list of HTML
        count = 1

        for element in definitions_html:
            words = element.text.split()
            if all([x.isdigit() for x in words]):
                count = 0
            if count == 2:
                definitions_list.append(element.text)
                examples_list.append(None)
            elif count == 3:
                examples_list[-1] = element.text
            count += 1
    if examples:
        assert(len(examples_list) == len(definitions_list))
        return list(zip(definitions_list, examples_list))
    else:
        return definitions_list


def get_definitions(word, examples=False):
    url = f'https://dlc.iec.cat/results.asp?txtEntrada={word}'
    soups = get_soup(url, word)
    definitions = scrap_definitions(soups, word, examples)
    return definitions


if __name__ == "__main__":
    word = "cartera"
    definitions_list = get_definitions(word, examples=True)
    for d, e in definitions_list:
        print(d, e)

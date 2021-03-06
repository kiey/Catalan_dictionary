import argparse
import os
import re
import multiprocessing
import functools
import traceback
from bs4 import element
from bs4 import BeautifulSoup
import requests
from concurrent import futures
from tqdm import tqdm
import urllib.parse as urlparse
from urllib.parse import parse_qs

import exceptions

DEBUG = False


def remove_accentuation(txt):
    txt_without_indexes = remove_superindexes_spaces(txt)
    accents = {ord('à'): 'a', ord('è'): 'e', ord('é'): 'e', ord('í'): 'i',
               ord('ò'): 'o', ord('ó'): 'o', ord('ú'): 'u', ord('ï'): 'i',
               ord('ü'): 'u'}
    return txt_without_indexes.translate(accents)


def remove_superindexes_spaces(txt):
    return re.sub("[²³¹⁰⁴⁵⁶⁷⁸⁹ ]", '', txt)


def get_ids(soup, word):
    """Get all the id of the words that are equal at the word passed, if none
    found return the first one. For example return "meu" if asking for "meva".
    """
    ids = []
    for html in soup.find_all(class_='resultAnchor'):
        if (remove_accentuation(word) == remove_accentuation(html.text) and
                word == remove_superindexes_spaces(html.text)):
            ids.append(html['id'])

    if not ids:
        html = soup.find(class_='resultAnchor')
        ids.append(html['id'])
    return ids

def get_lemma(url, word):
    html_get = requests.get(url)
    soup_get = BeautifulSoup(html_get.text, 'html.parser')
    if DEBUG:
        with open(f'../logs/{word}_syllables_get.html', 'w') as f:
            f.write(soup_get.prettify())

    lemmas = soup_get.find_all('a')
    if len(lemmas) == 1:
        return lemmas[0].get('href')
    for lemma in lemmas:
        if (word == lemma.text):
            return lemma.get('href')
    raise exceptions.WordNotFoundError(word)




def get_syllables(word):
    """ Given a word it returns a list containing the syllabes splitted and the index of the tonic syllable"""
    base_url = 'http://ca.oslin.org/'
    url = f'http://ca.oslin.org/index.php?sel=exact&query={word}&action=simplesearch&base=form'

    lemma_url = get_lemma(url, word)
    url = base_url + lemma_url
    html_get = requests.get(url)
    soup_get = BeautifulSoup(html_get.text, 'html.parser')

    definitions_html = soup_get.find(class_='syllables')

    syllabes_list = definitions_html.text.split('·')
    count = 0
    for a in definitions_html:
        if (type(a) is element.NavigableString):
            count += 1
        if str(a).startswith('<u>'):
            break

    return syllabes_list, count



def get_definitions_soup(url, word):
    """ Given a url from the a word in the DIEC2, it retrieves the html contai
    ning the definitons"""
    html_get = requests.get(url)
    soup_get = BeautifulSoup(html_get.text, 'html.parser')

    if DEBUG:
        with open(f'../logs/{word}_get.html', 'w') as f:
            f.write(soup_get.prettify())

    definitions_html = soup_get.find(class_="resultDefinition")
    not_found = "No s'ha trobat cap entrada coincident amb els criteris de cerca"
    if (definitions_html.text == not_found):
        raise exceptions.WordNotFoundError(word)

    ids = get_ids(soup_get, word)
    if (len(ids) == 0):
        raise exceptions.WordNotFoundError(word)

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
        #print(definitions_html)

        for element in definitions_html:
            words = element.text.split()
            if not words:
                continue
            if (words[0][0] == '['):
                continue
            if all([x.isdigit() for x in words]):
                count = 0
            if count == 1:
                definitions_list.append(element.text.strip())
                examples_list.append(None)
            elif count == 2:
                examples_list[-1] = element.text.strip()
            count += 1
    if(len(definitions_list) == 0):
        raise exceptions.WordNotFoundError(word)
    assert(len(examples_list) == len(definitions_list))

    if examples:
        return list(zip(definitions_list, examples_list))
    else:
        return definitions_list


def get_definitions(word, examples=False):
    if not word.strip():
        raise exceptions.WordNotFoundError(word)
    url = f'https://dlc.iec.cat/results.asp?txtEntrada={word}'
    try:
        soups = get_definitions_soup(url, word)
    except requests.exceptions.ConnectionError as e:
        raise exceptions.ConnectionError() from e
    definitions = scrap_definitions(soups, word, examples)
    return definitions


def get_definitions_list(shared_definitons, shared_exceptions, words, pbar, i, examples=False):
    try:
        shared_definitons[i] = get_definitions(words[i], examples)
    except IndexError as e:
        # Output expected IndexErrors.
        print(i, word, len(shared_definitons), len(words))
        Logging.log_exception(error)
    except Exception as e:
        shared_exceptions.append((words[i], f'{type(e).__name__}'))
        raise e
    finally:
        pbar.update(1)


def get_definitions_bulk(words, examples=False, num_threads=20, progress=True):
    mum_threads = min(num_threads, 100)
    with futures.ThreadPoolExecutor(num_threads) as executor:  # Create a pool of worker processes
        manager = multiprocessing.Manager()  # Create a manager to handle shared object(s).
        # Create a proxy for the shared list object.
        if examples:
            print("examples")
            shared_definitions = manager.list([None, None] * len(words))
        else:
            print("No examples")
            shared_definitions = manager.list([None] * len(words))
        shared_exceptions = manager.list()

        pbar = tqdm(disable=not progress, total=len(words))

        # Create a single arg function with the first positional argument (arr) supplied.
        # (This is necessary because Pool.map() only works with functions of one argument.)
        mono_arg_func = functools.partial(get_definitions_list, shared_definitions,
                                          shared_exceptions, words, pbar, examples=examples)
        exceptions_map = executor.map(mono_arg_func, range(len(shared_definitions)))
        #  for e in exceptions_map:
        #     pass
        return shared_definitions, shared_exceptions


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="stores html files in ../log", action="store_true")
    args = parser.parse_args()
    DEBUG = args.debug
    if args.debug:
        print("DEBUG ON")
        if DEBUG and not os.path.exists('../logs'):
            os.makedirs('../logs')
    word = "tassa"
    print(get_definitions(word))
    word = "seva"
    print(get_definitions(word))

    """
    
    word = "tassa"
    url = 'http://ca.oslin.org/index.php?action=lemma&lemma=3754'
    print(get_syllables(word))
    print('-' * 80)
    word = "cantar"
    url = 'http://ca.oslin.org/index.php?action=lemma&lemma=3754'
    print(get_syllables(word))
    print('-' * 80)
    word = "clau"
    url = 'http://ca.oslin.org/index.php?action=lemma&lemma=3754'
    print(get_syllables(word))
    definitions_list = get_definitions(word, examples=True)
    for d, e in definitions_list:
        print(d, e)
    """
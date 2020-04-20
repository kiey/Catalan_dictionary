from selenium import webdriver
import bs4
import time
import itertools
import exceptions
import requests


# export PATH="$PATH:/home/joan/tests/"

def get_soup_POST(url, word):
    html_get = requests.get(url)
    soup_get = bs4.BeautifulSoup(html_get.text, 'html.parser')

    definitions_html = soup_get.find(class_="resultDefinition")  # interesting part of the HTML
    not_found = "No s'ha trobat cap entrada coincident amb els criteris de cerca"
    if (definitions_html.text == not_found):
        raise exceptions.WordNotFoundError(f'{word} not found')

    id = soup_get.find(class_='resultAnchor')['id']
    params = {'id': id, 'searchParam': word}
    url_post = 'https://dlc.iec.cat/Results/Accepcio'

    html_post = requests.post(url_post, data=params)
    soup_post = bs4.BeautifulSoup(html_post.text, 'html.parser')
    return soup_post


def get_webpage(url):
    driver = webdriver.Firefox('./')
    driver.get(url)

    time.sleep(1)  # wait for javascript to run

    htmlSource = driver.page_source
    driver.quit()

    return(str(htmlSource))  # To Do: check if cast to string is necessary


def scrap_definitions(soup, word, examples=False):
    """
    Given the soup of the IEC webpage of a word it retrieves a list of the definitions.
    If example is true, a list of tupples (definition,example) will be retrieved.
    If a definition has no examples, the value returned is None.
    """
    definitions_html = soup.find(class_="resultDefinition")  # interesting part of the HTML
    not_found = "No s'ha trobat cap entrada coincident amb els criteris de cerca"
    if (definitions_html.text == not_found):
        raise exceptions.WordNotFoundError(f'{word} not found')
    definitions_html = soup.find_all(name='span', class_="body")  # list of HTML
    count = 0
    definitions_list = []
    examples_list = []

    for element in definitions_html:
        words = element.text.split()
        if all([x.isdigit() for x in words]):
            count = 0
        if count == 2:
            definitions_list.append(element.text)
        elif count == 3:
            examples_list.append(element.text)
        count += 1
    if examples:
        return itertools.zip_longest(definitions_list, examples_list)
    return definitions_list


def scrap_definitions_POST(soup, word, examples=False):
    """
    Given the soup of the IEC webpage of a word it retrieves a list of the definitions.
    If example is true, a list of tupples (definition,example) will be retrieved.
    If a definition has no examples, the value returned is None.
    """

    definitions_html = soup.find_all(name='span', class_="\\\"body\\\"")  # list of HTML
    count = 0
    definitions_list = []
    examples_list = []

    for element in definitions_html:
        words = element.text.split()
        if all([x.isdigit() for x in words]):
            count = 0
        if count == 2:
            definitions_list.append(element.text)
        elif count == 3:
            examples_list.append(element.text)
        count += 1
    if examples:
        return list(itertools.zip_longest(definitions_list, examples_list))
    else:
        return definitions_list


def get_definitions(word, examples=False):
    url = f'https://dlc.iec.cat/results.asp?txtEntrada={word}'
    soup_post = get_soup_POST(url, word)
    definitions = scrap_definitions_POST(soup_post, word, examples)
    return definitions


if __name__ == "__main__":
    word = "cantar"
    definitions_list = get_definitions(word, examples=True)
    for d, e in definitions_list:
        print(e)


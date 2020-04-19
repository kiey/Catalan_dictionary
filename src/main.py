from selenium import webdriver
import bs4
import time
import itertools
import exeptions


# export PATH="$PATH:/home/joan/tests/"
def get_webpage(url):

    driver = webdriver.Firefox('./')
    driver.get(url)
    time.sleep(1)
    htmlSource = driver.page_source
    driver.quit()

    with open('iec_cantar.txt', 'w') as f:
        f.write(str(htmlSource))


def get_definitions(soup, word, examples=False):
    "To do: implement tests, handle exeptions word not found"
    """
    Given the soup of the IEC webpage of a word it retrieves a list of the definitions.
    If example is true, a list of tupples (definition,example) will be retrieved.
    If a definition has no examples, the value returned is None.
    """
    definitions_html = soup.find(class_="resultDefinition")  # interesting part of the HTML
    not_found = "No s'ha trobat cap entrada coincident amb els criteris de cerca"
    if (definitions_html.text == not_found):
        raise exeptions.WordNotFoundError(f'{word} not found')
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
        print(examples_list)
        return itertools.zip_longest(definitions_list, examples_list)
    return definitions_list


if __name__ == "__main__":

    word = "afefe"
    url = f'https://dlc.iec.cat/results.asp?txtEntrada={word}'
    # get_webpage(url)
    with open('iec_cantar.txt', 'r') as f:
        soup = bs4.BeautifulSoup(f.read(), 'html.parser')
    definitions = get_definitions(soup, word, examples=True)
    for d, e in definitions:
        print(d, e)

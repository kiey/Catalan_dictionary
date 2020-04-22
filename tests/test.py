import re
import sys
sys.path.append("..")
sys.path.append("../src")

import pytest

import catalanDictionary
import exceptions 


def test_basic():
    word = 'ordinador'
    definitions = catalanDictionary.get_definitions(word, examples=True)
    definitions_unzipped = [[i for i, j in definitions],
                            [j for i, j in definitions]]
    assert(len(definitions_unzipped[0]) == 2)
    assert(all(definitions_unzipped[0]))
    assert(len(definitions_unzipped[1]) == 2)
    assert(any(definitions_unzipped[1]))

    assert(definitions[0][0] == 'Màquina electrònica digital que permet el pr'
                                'ocessament automàtic, l’obtenció, l’emmagatz'
                                'ematge, la transformació i la comunicació de'
                                ' la informació mitjançant programes preestab'
                                'lerts.')
    assert(definitions[0][1] == 'Ordinador central.')


def test_only_one_definiton():
    word = 'bicicleta'
    definitions = catalanDictionary.get_definitions(word)
    assert(len(definitions) == 1)
    print(definitions[0])
    assert(definitions[0] == 'Vehicle lleuger de dues rodes, unides per un quad'
                             're, la del davant directora i la del darrere m'
                             'otora, que s’acciona amb pedals.')


def test_only_one_definiton_exemples():
    word = 'bicicleta'
    definitions = catalanDictionary.get_definitions(word, examples=True)
    assert(len(definitions) == 1)
    assert(definitions[0][0] == 'Vehicle lleuger de dues rodes, unides per un quad'
                                're, la del davant directora i la del darrere m'
                                'otora, que s’acciona amb pedals.')
    assert(definitions[0][1] == 'Bicicleta de muntanya.')


def test_only_get_word_same_accentuation():
    word1 = 'cantar'
    definitions = catalanDictionary.get_definitions(word1)
    assert(len(definitions) == 20)
    assert(all(definitions))

    definitions = catalanDictionary.get_definitions(word1, examples=True)
    definitions_unzipped = [[i for i, j in definitions],
                            [j for i, j in definitions]]
    assert(len(definitions_unzipped[0]) == 20)
    assert(all(definitions_unzipped[0]))
    assert(len(definitions_unzipped[1]) == 20)
    assert(any(definitions_unzipped[1]))
    assert(definitions[19][0] == 'Fer pudor.')
    assert(definitions[19][1] == 'Li canten els peus.')

    word2 = 'càntar'
    definitions = catalanDictionary.get_definitions(word2)
    assert(len(definitions) == 1)
    assert(all(definitions))


def test_word_with_different_name_entries():
    word = 'cartera'
    definitions = catalanDictionary.get_definitions(word, examples=True)
    definitions_unzipped = [[i for i, j in definitions],
                            [j for i, j in definitions]]
    assert(len(definitions_unzipped[0]) == 12)
    assert(len(definitions_unzipped[1]) == 12)
    assert(any(definitions_unzipped[1]))


def test_WordNotFoundError():
    word = "abcdf"
    with pytest.raises(exceptions.WordNotFoundError):
        definitions = catalanDictionary.get_definitions(word, examples=True)

def test_long_text():
    text = ("Twain fou un personatge molt conegut a la seva època, i va ser amic de"
           " presidents, artistes, grans empresaris, i membres de la reialesa euro"
           "pea. Pel seu enginy i talent per a la sàtira va ser molt popular. En e"
           "l moment de la seva mort, se'l va considerar \"l'humorista americà més "
           "gran de la seva època\",[2] i William Faulkner el va anomenar «el pare "
           "de la literatura americana».")

    words_not_found = []
    words_found = []

    for word in (re.split(r'\W+', text)):
        try:
            definitions = catalanDictionary.get_definitions(word, examples=True)
            assert(len(definitions) > 0)
            words_found.append(word)
        except exceptions.WordNotFoundError:
            words_not_found.append(word)
        except exceptions.EmptyStrError:
            pass

    assert(len(words_not_found) == 7)
    assert(len(words_found) == 65)


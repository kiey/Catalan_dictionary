import sys
sys.path.append("..")
sys.path.append("../src")

import pytest

import bs4

import catalanDictionary
import exceptions 


def test_bicicleta():
    word = 'bicicleta'
    definitions = catalanDictionary.get_definitions(word)
    assert(len(definitions) == 1)
    print(definitions[0])
    assert(definitions[0] == 'Vehicle lleuger de dues rodes, unides per un quad'
                             're, la del davant directora i la del darrere m'
                             'otora, que s’acciona amb pedals. ')


def test_bicicleta_exemples():
    word = 'bicicleta'
    definitions = catalanDictionary.get_definitions(word, examples=True)
    assert(len(definitions) == 1)
    assert(definitions[0][0] == 'Vehicle lleuger de dues rodes, unides per un quad'
                                're, la del davant directora i la del darrere m'
                                'otora, que s’acciona amb pedals. ')
    assert(definitions[0][1] == 'Bicicleta de muntanya.')


def test_cantar():
    word = 'cantar'
    definitions = catalanDictionary.get_definitions(word)
    assert(len(definitions) == 21)
    assert(all(definitions))


def test_cantar_examples():
    word = 'cantar'
    definitions = catalanDictionary.get_definitions(word, examples=True)
    definitions_unzipped = [[i for i, j in definitions],
                            [j for i, j in definitions]]
    assert(len(definitions_unzipped[0]) == 21)
    assert(all(definitions_unzipped[0]))
    assert(len(definitions_unzipped[1]) == 21)
    assert(any(definitions_unzipped[1]))
    assert(definitions[19][0] == 'Fer pudor. ')
    for d, e in definitions:
        print(d, e)
    assert(definitions[19][1] == 'Li canten els peus.')


def test_cartera_examples():
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

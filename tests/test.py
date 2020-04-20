import sys
sys.path.append("..")
sys.path.append("../src")

import pytest

import bs4

import catalanDictionary
import exceptions 


def test_cantar():
    word = 'cantar'
    definitions = catalanDictionary.get_definitions(word)
    assert(len(definitions) == 20)


def test_cantar_examples():
    word = 'cantar'
    definitions = catalanDictionary.get_definitions(word, examples=True)
    definitions_unzipped = [[i for i, j in definitions],
                            [j for i, j in definitions]]
    assert(len(definitions_unzipped[0]) == 20)
    assert(len(definitions_unzipped[1]) == 20)
    assert(all(definitions_unzipped[1]))


def test_WordNotFoundError():
    word = "abcdff"
    with pytest.raises(exceptions.WordNotFoundError):
        definitions = catalanDictionary.get_definitions(word, examples=True)


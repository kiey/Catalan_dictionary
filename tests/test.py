import sys
sys.path.append("..")
sys.path.append("../src")

import pytest

import bs4

import main as catalan_dictionary
import exceptions 


def test_cantar():
    word = 'cantar'
    definitions = catalan_dictionary.get_definitions(word)
    assert(len(definitions) == 20)


def test_cantar_examples():
    word = 'cantar'
    definitions = catalan_dictionary.get_definitions(word, examples=True)
    assert(len(list(definitions)) == 20)


def test_WordNotFoundError():
    word = "abcdff"
    with pytest.raises(exceptions.WordNotFoundError):
        definitions = catalan_dictionary.get_definitions(word, examples=True)


test_WordNotFoundError()
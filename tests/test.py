import re
import sys
sys.path.append("..")
sys.path.append("../src")

import pytest

import catalanDictionary as catDic
import exceptions 


def test_basic():
    word = 'ordinador'
    definitions = catDic.get_definitions(word, examples=True)
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
    definitions = catDic.get_definitions(word)
    assert(len(definitions) == 1)
    print(definitions[0])
    assert(definitions[0] == 'Vehicle lleuger de dues rodes, unides per un quad'
                             're, la del davant directora i la del darrere m'
                             'otora, que s’acciona amb pedals.')


def test_only_one_definiton_exemples():
    word1 = 'bicicleta'
    definitions = catDic.get_definitions(word1, examples=True)
    assert(len(definitions) == 1)
    assert(definitions[0][0] == 'Vehicle lleuger de dues rodes, unides per un quad'
                                're, la del davant directora i la del darrere m'
                                'otora, que s’acciona amb pedals.')
    assert(definitions[0][1] == 'Bicicleta de muntanya.')

    word2 = 'va'
    definitions = catDic.get_definitions(word2, examples=True)
    assert(len(definitions) == 6)
    assert(definitions[0][0] ==
        'Auxiliar del passat perifràstic i del passat anterior perifràstic d’indicatiu.')
    assert(definitions[0][1] == 'Vaig caure.')


def test_only_get_word_same_accentuation():
    word1 = 'cantar'
    definitions = catDic.get_definitions(word1)
    assert(len(definitions) == 20)
    assert(all(definitions))

    definitions = catDic.get_definitions(word1, examples=True)
    definitions_unzipped = [[i for i, j in definitions],
                            [j for i, j in definitions]]
    assert(len(definitions_unzipped[0]) == 20)
    assert(all(definitions_unzipped[0]))
    assert(len(definitions_unzipped[1]) == 20)
    assert(any(definitions_unzipped[1]))
    assert(definitions[19][0] == 'Fer pudor.')
    assert(definitions[19][1] == 'Li canten els peus.')

    word2 = 'càntar'
    definitions = catDic.get_definitions(word2)
    assert(len(definitions) == 1)
    assert(all(definitions))


def test_word_with_different_name_entries():
    word = 'cartera'
    definitions = catDic.get_definitions(word, examples=True)
    definitions_unzipped = [[i for i, j in definitions],
                            [j for i, j in definitions]]
    assert(len(definitions_unzipped[0]) == 12)
    assert(len(definitions_unzipped[1]) == 12)
    assert(any(definitions_unzipped[1]))


def test_WordNotFoundError():
    word = "abcdf"
    with pytest.raises(exceptions.WordNotFoundError):
        catDic.get_definitions(word, examples=True)


def test_long_text():
    with open('texts/Twain.txt', 'r') as f:
        text = f.read()
    words_not_found = []
    words_found = []

    for word in (re.split(r'\W+', text)):
        try:
            definitions = catDic.get_definitions(word, examples=True)
            assert(len(definitions) > 0)
            words_found.append(word)
        except exceptions.WordNotFoundError:
            words_not_found.append(word)
        except exceptions.EmptyStrError:
            pass

    assert(len(words_not_found) == 8)
    assert(len(words_found) == 65)


def test_cervantes_bulk():
    with open('texts/Cervantes.txt', 'r') as f:
        text = f.read()

    words = re.split(r'\W+', text)

    words_definitions, exceptions_bulk = catDic.get_definitions_bulk(words, num_threads=30)
    for word, error in exceptions_bulk:
        assert(error == "WordNotFoundError")

    assert(len(exceptions_bulk) <= 127)
    for word_definitions in words_definitions:
        assert(word_definitions is None or any(word_definitions))


def test_same_output_concurrent():
    with open('texts/Cervantes.txt', 'r') as f:
        text = f.readline()

    words = re.split(r'\W+', text)
    words_defs_conc, _ = catDic.get_definitions_bulk(words, num_threads=30)
    word_defs_ser = []
    for word in words:
        try:
            word_defs_ser.append(catDic.get_definitions(word))
        except exceptions.WordNotFoundError:
            word_defs_ser.append(None)
    assert(len(words_defs_conc) == len(word_defs_ser))
    for word_defs_conc, word_defs_ser, word in zip(words_defs_conc, word_defs_ser, words):
        assert((word_defs_conc is None) == (word_defs_ser is None))
        if word_defs_conc and word_defs_ser:
            for def_conc, def_ser in zip(word_defs_conc, word_defs_ser):
                assert(def_conc == def_ser)


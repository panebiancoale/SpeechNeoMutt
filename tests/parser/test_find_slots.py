import pytest
from parser.parser import parser_command
from unittest import mock

class TestFindSlots:
    """
    Classe per verificare il corretto funzionamento del modulo trova 'slots' nel testo di input
    """
    @pytest.mark.parametrize("text,expected_dest,expected_subject,expected_body", [
        ("scrivi a bob e tom con oggetto prova testo prova",["bob@example.com","tom@example.com"],"prova","prova"),
        ("scrivi a bob",["bob@example.com"],None,None),
        ("scrivi a bob con oggetto prova",["bob@example.com"],"prova",None),
        ("scrivi a bob testo prova",["bob@example.com"],None,"prova"),
        ("scrivi con oggetto prova",None,"prova",None),
        ("scrivi testo prova",None,None,"prova"),
        ("scrivi con oggetto prova testo prova",None,"prova","prova")
    ])
    def test_write_email(self,text,expected_dest,expected_subject,expected_body):
        """
        Testa il corretto riconoscimento degli elementi nel testo parsato per modulo 'write_email'
        :param text: testo di input
        :param expected_dest: destinatario/i atteso/i
        :param expected_subject: oggetto atteso
        :param expected_body: testo atteso
        :return:
        """
        test_alias = {
            "bob": "bob@example.com",
            "tom": "tom@example.com"
        }
        with mock.patch("actions.email.ALIAS_TO_ADDR", test_alias):
            data = parser_command(text)
            slots = data.get("slots",{})
            assert slots.get("dest") == expected_dest
            assert slots.get("subject") == expected_subject
            assert slots.get("body") == expected_body

    @pytest.mark.parametrize("text,expected_index",[
        ("leggi la prima email",1),
        ("leggi la mail numero uno",1)
    ])
    def test_read_email(self,text,expected_index):
        """
        Testa il corretto riconoscimento degli elementi nel testo parsato per modulo 'read_email'
        :param text: testo di input
        :param expected_index: indice atteso
        :return:
        """
        data = parser_command(text)
        slots = data.get("slots",{})
        assert slots.get("index") == expected_index

    @pytest.mark.parametrize("text,expected_pos,word_limit",[
        ("aggiungi alla fine","end",None),
        ("aggiungi all'inizio","start",None),
        ("aggiungi dopo ciao","after","ciao"),
        ("aggiungi dopo","after",None),
        ("aggiungi dopo il punto","after","punto"),
        ("aggiungi prima","before",None),
        ("aggiungi prima di ciao","before","ciao")
    ])
    def test_add_subject(self,text,expected_pos,word_limit):
        """
        Testa il corretto riconoscimento della posizione
        :param text: testo di input
        :param expected_pos: posizione attesa
        :param word_limit: parola specificata
        :return:
        """
        data = parser_command(text)
        slots = data.get("slots",{})
        assert slots.get("word_limit") == word_limit
        assert slots.get("position") == expected_pos

    @pytest.mark.parametrize("text,replace_word,expected_word",[
        ("sostituisci ciao con buongiorno","ciao","buongiorno"),
        ("sostituisci ciao","ciao",None),
        ("sostituisci la virgola con il punto di domanda","virgola","punto di domanda")
    ])
    def test_replace_word(self,text,replace_word,expected_word):
        """
        Testa il corretto funzionamento del modulo 'replace_word'
        :param text: testo di input
        :param replace_word: parola da sostituire
        :param expected_word: parola attesa
        :return:
        """
        data = parser_command(text)
        slots = data.get("slots",{})
        assert slots.get("word_to_replace") == replace_word
        assert slots.get("new_word") == expected_word

    @pytest.mark.parametrize("text,expected_word", [
        ("cancella buongiorno", "buongiorno"),
        ("cancella la virgola", "virgola"),
        ("cancella ciao come va","ciao come va"),
    ])
    def test_delete_word(self,text,expected_word):
        """
        Testa il corretto funzionamento del modulo 'delete_word'
        :param text: testo di input
        :param expected_word: parola attesa
        :return:
        """
        data = parser_command(text)
        slots = data.get("slots",{})
        assert slots.get("word_to_delete") == expected_word



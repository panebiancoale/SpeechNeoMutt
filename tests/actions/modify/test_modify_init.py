import pytest
from actions.email.modify import delete_word, replace_word, add_word_after, add_word_before
from unittest import mock


class TestInit:
    """
    Testa i metodi del modulo '__init__' del package 'modify'
    """
    @pytest.mark.parametrize("current_text,slots,expected_text", [
        ("ciao, come va",{'word_to_delete':'virgola'},"ciao come va"),
    ])
    def test_delete_word(self,current_text,slots,expected_text):
        """
        Testa il corretto funzionanemento dell'eliminazione di una parola, considerando anche i simboli di punteggiatura
        :param current_text: testo corrente
        :param slots: contiene le variabili necessarie
        :param expected_text: testo atteso
        :return:
        """
        with mock.patch("actions.email.modify.text_to_speech.text_to_speech") as stt:
            new_text = delete_word(current_text,slots)
            assert new_text == expected_text
            args,kwargs = stt.call_args
            assert args[0] == "Parola eliminata correttamente"

    @pytest.mark.parametrize("current_text,slots,expected_text", [
        ("ciao, come va?",{'word_to_replace':'ciao','new_word':'buongiorno a tutti'},"buongiorno a tutti, come va?"),
    ])
    def test_replace_word(self,current_text,slots,expected_text):
        """
        Testa il corretto funzionamento della sostituzione di una parola
        :param current_text: testo corrente
        :param slots: contiene le variabili necessarie
        :param expected_text: testo atteso
        :return:
        """
        with mock.patch("actions.email.modify.text_to_speech.text_to_speech") as stt:
            new_text = replace_word(current_text,slots)
            assert new_text == expected_text
            args,kwargs = stt.call_args
            assert args[0] == "Parola sostituita correttamente"

    @pytest.mark.parametrize("current_text,word_limit,new_part,expected_text", [
        ("ciao, a che ora è la","la","partita?","ciao, a che ora è la partita?"),
        ("ciao come va?","ciao",",","ciao, come va?"),
        ("ciao,","virgola","come va?","ciao, come va?"),
        ("ciao, come va?","punto di domanda","spero tutto bene","ciao, come va? spero tutto bene"),
    ])
    def test_add_word_after(self,current_text,word_limit,new_part,expected_text):
        """
        Testa il corretto funzionamento dell'aggiunta di una parola dopo un'altra
        :param current_text: testo corrente
        :param word_limit: parola 'limite' dopo la quale bisogna aggiungere
        :param new_part: nuova parte del testo
        :param expected_text: testo atteso
        :return:
        """
        new_text = add_word_after(current_text,word_limit,new_part)
        assert new_text == expected_text

    @pytest.mark.parametrize("current_text,word_limit,new_part,expected_text", [
        ("ciao, come va?","virgola","a tutti","ciao a tutti, come va?"),
        ("a che ora è la partita?","a","buongiorno,","buongiorno, a che ora è la partita?"),
    ])
    def test_add_word_before(self,current_text,word_limit,new_part,expected_text):
        """
        Testa il corretto funzionamento dell'aggiunta di una parola prima di un'altra
        :param current_text: testo corrente
        :param word_limit: parola 'limite' prima della quale bisogna aggiungere
        :param new_part: nuova parte del testo
        :param expected_text: testo atteso
        :return:
        """
        new_text = add_word_before(current_text,word_limit,new_part)
        assert new_text == expected_text


import pytest
from unittest import mock
from actions.email.modify.add_body import add_body


class TestAddBody:
    """
    Testa il funzionamento del modulo 'add_body'
    """
    @pytest.mark.parametrize("current_body,slots,new_body_part,expected_body", [
        ("ciao",{},"virgola come va","ciao, come va"),
        ("ciao",{},"come va","ciao come va"),
        ("ciao",{},"a capo come va","ciao \ncome va")
    ])
    def test_add_body_with_punctuation_at_the_end(self,current_body,slots,new_body_part,expected_body):
        """
        Testa il corretto funzionamento dell'aggiunta di testo, facendo un concatenamento con quello corrente
        :param current_body: testo corrente
        :param slots: contiene variabili necessarie per il posizionamento, di defult si utilizza posizione 'end'
        :param new_body_part: la nuova parte di testo da aggiungere
        :param expected_body: testo atteso
        :return:
        """
        with mock.patch("actions.email.ask_user_or_stop", return_value=new_body_part),\
             mock.patch("actions.email.confirm_input", return_value=True):
            new_body = add_body(current_body,slots)
            assert new_body == expected_body

    @pytest.mark.parametrize("current_body,slots,new_body_part,expected_body", [
        ("ciao come va",{'position':'after','word_limit':'ciao'},"virgola","ciao, come va"),
        ("ciao,",{'position':'after','word_limit':'virgola'},"come va","ciao, come va"),
        ("ok perfetto.",{'position':'after','word_limit':'punto semplice'},"a capo buona giornata","ok perfetto. \nbuona giornata"),
    ])
    def test_add_body_with_punctuation_after_word(self,current_body,slots,new_body_part,expected_body):
        """
        Testa il corretto funzionamento dell'aggiunta di testo dopo una parola
        :param current_body: testo corrente
        :param slots: contiene variabili necessarie per il posizionamento, di defult si utilizza posizione 'end'
        :param new_body_part: la nuova parte di testo da aggiungere
        :param expected_body: testo atteso
        :return:
        """
        with mock.patch("actions.email.ask_user_or_stop", return_value=new_body_part),\
             mock.patch("actions.email.confirm_input", return_value=True):
            new_body = add_body(current_body,slots)
            assert new_body == expected_body


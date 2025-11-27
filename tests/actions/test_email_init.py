import pytest
from unittest import mock
from actions.email import get_body

class TestEmailInit:
    """
    Classe per testare il modulo '__init__' di email
    """
    @pytest.mark.parametrize("original_text,expected_text",[
        ("Ciao come va punto di domanda","Ciao come va?"),
        ("Arrivo punto esclamativo Un minuto","Arrivo! Un minuto"),
        ("ciao virgola la riunione è alle cinque","ciao, la riunione è alle cinque"),
        ("ciao invio come va","ciao \n come va"),
        ("a capo come va","\n come va")
    ])
    def test_get_body(self,original_text,expected_text):
        """
        Test per verificare il corretto funzionamento della funzione 'get_body'
        :param original_text: testo passato come input
        :param expected_text: testo attesto
        :return:
        """
        with mock.patch("actions.email.ask_user_or_stop",return_value=original_text):
            body = get_body()
            assert body == expected_text
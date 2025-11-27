import pytest
from parser.parser import parser_command

class TestFindIntent:
    """
    Classe per verificare il corretto funzionamento del modulo trova 'intent' nel testo di input
    """
    @pytest.mark.parametrize("text,expected_intent",[
        ("scrivi","write_email"),
        ("leggi","read_email"),
        ("rispondi","reply_email"),
        ("nuove","notify_new_inbox"),
        ("novità","notify_new_inbox"),
        ("modifica destinatario","modify_dest"),
        ("modifica destinatari","modify_dest"),
        ("modifica oggetto","modify_subject"),
        ("modifica testo","modify_body"),
        ("aggiungi destinatario","add_dest"),
        ("aggiungi destinatari","add_dest"),
        ("rileggi","read_again"),
        ("sostituisci","replace_word"),
        ("cambia","rewrite"),
        ("cancella","delete_word")
    ])
    def test_find_intent(self, text, expected_intent):
        """
        Testa il corretto riconoscimento degli intent nel testo parsato
        :param text: testo di input
        :param expected_intent: intent atteso
        :return:
        """
        data = parser_command(text)
        assert data.get("intent") == expected_intent
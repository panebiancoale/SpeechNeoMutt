import logging
from unittest import mock
from actions.actions_executor import execute
from parser.parser import parser_command
from services.core import state,context
import actions.email.general.write_email as write
class TestWriteEmail:
    """
    Classe di test per verificare il corretto funzionamento del flusso scrivi nuova email
    """
    def test_write_email_success(self):
        """
        Testa il modulo 'write_email' con invio riuscito
        :return:
        """
        input_stt = parser_command("scrivi a tesi con oggetto oggetto di prova testo testo di prova")
        state.pending_intent = input_stt.get("intent")
        state.slots = input_stt.get("slots")

        with mock.patch.object(write,"_confirm_and_send",return_value=True) as confirm_email:
            execute(input_stt,state,context)

            assert confirm_email.called
            args, kwargs = confirm_email.call_args
            dest_list,subject,body = args

            assert dest_list == ["tesi.neomutt@gmx.com"]
            assert subject == "oggetto di prova"
            assert body == "testo di prova"

    def test_write_email_failure(self):
        """
        Testa il modulo 'write_email' con invio fallito
        :return:
        """
        input_stt = parser_command("scrivi a tesi con oggetto oggetto di prova testo testo di prova")
        state.pending_intent = input_stt.get("intent")
        state.slots = input_stt.get("slots")

        with mock.patch.object(write, "_confirm_and_send", return_value=False) as unconfirm_email:
            execute(input_stt, state, context)

            assert unconfirm_email.called


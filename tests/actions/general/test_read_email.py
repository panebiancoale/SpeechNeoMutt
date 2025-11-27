import os
import time
import pytest
from email.message import EmailMessage
from email.utils import formatdate, make_msgid
from pathlib import Path
from actions.actions_executor import execute
from config import INBOX_DIR, HOSTNAME
from parser.parser import parser_command
from services.core import state, context
from unittest import mock

class TestReadEmail:
    """
    Classe di test per verificare il corretto funzionamento del modulo leggi email
    """
    @pytest.fixture(autouse=False)
    def clean_state(self):
        """
        Utilizzato per mantenere indipendenti i test quando richiesto
        :return:
        """
        state.pending_intent = None
        state.slots = {}
        if context.current_email:
            email_to_unlink = context.current_email
            tmp_email = Path.home() / INBOX_DIR / "cur" / email_to_unlink["email"]
            tmp_email.unlink()
            context.current_email = None
        context.new_inbox_emails = []
        context.save()

    def test_read_email_success(self):
        """
        Test di successo per il modulo 'read_email'
        :return:
        """
        sender = "bob@example.com"
        dest = ['tesi.neomutt@gmx.com']
        subject = "oggetto di prova"
        body = "testo di prova"

        email_to_read = self.create_tmp_email(sender, dest, subject, body)
        self.update_context(email_to_read)
        input_stt = parser_command("leggi")
        state.pending_intent = input_stt.get("intent")
        state.slots = input_stt.get("slots")

        with mock.patch("actions.email.general.read_email.text_to_speech.text_to_speech") as read_email:
            execute(input_stt, state, context)

            assert read_email.called
            args, kwargs = read_email.call_args

            text_msg = args[0]
            assert sender in text_msg
            assert subject in text_msg
            assert body in text_msg

    def test_read_again_success(self):
        """
        Test di successo per il modulo 'read_again'
        :return:
        """
        sender = "bob@example.com"
        subject = "oggetto di prova"
        body = "testo di prova"

        input_stt = parser_command("rileggi")
        state.pending_intent = input_stt.get("intent")
        state.slots = input_stt.get("slots")

        with mock.patch("actions.email.general.read_email.text_to_speech.text_to_speech") as read_again:
            execute(input_stt, state, context)

            assert read_again.called
            args, kwargs = read_again.call_args
            text_msg = args[0]
            assert sender in text_msg
            assert subject in text_msg
            assert body in text_msg


    def test_read_email_failure(self,clean_state):
        """
        Test di fallimento per il modulo 'read_email' (Non ci sono email da leggere)
        :return:
        """
        input_stt = parser_command("leggi")
        state.pending_intent = input_stt.get("intent")
        state.slots = input_stt.get("slots")

        with mock.patch("actions.email.general.read_email.text_to_speech.text_to_speech") as read_email:
            execute(input_stt, state, context)

            assert read_email.called
            args, kwargs = read_email.call_args
            text_msg = args[0]
            assert "Non ci sono email da leggere" in text_msg


    def test_read_again_failure(self,clean_state):
        """
        Test di fallimento per il modulo 'read_again'
        :return:
        """
        input_stt = parser_command("rileggi")
        state.pending_intent = input_stt.get("intent")
        state.slots = input_stt.get("slots")

        with mock.patch("actions.email.general.read_email.text_to_speech.text_to_speech") as read_again:
            execute(input_stt, state, context)

            assert read_again.called
            args, kwargs = read_again.call_args
            text_msg = args[0]
            assert "Non ci sono email da leggere" in text_msg

    @staticmethod
    def create_tmp_email(sender,dest,subject,body):
        """
        Crea file per l'email da leggere
        :param sender: mittente
        :param dest: destinatario/i
        :param subject: oggetto
        :param body: testo
        :return: il percorso del file
        """
        msg = EmailMessage()
        msg["Date"] = formatdate(localtime=True)
        msg['From'] = sender
        msg["To"] = ", ".join(dest)
        msg["Subject"] = subject
        msg["Message-ID"] = make_msgid(domain="Neomutt-Tesi")
        msg.set_content(body)

        filename = f"{int(time.time())}.{os.getpid()}.{HOSTNAME}:2,"
        tmp_filepath = Path.home() / INBOX_DIR / "new" / filename

        with tmp_filepath.open("wb") as fp:
            fp.write(msg.as_bytes())

        return tmp_filepath

    @staticmethod
    def update_context(file_path):
        """
        Aggiorna il contesto per tener conto della nuova email
        :param file_path: percorso del file
        :return:
        """
        email_list = [{
            "folder": file_path.parent.name,
            "email": file_path.name
        }]
        context.current_email = {
            "folder":file_path.parent.name,
            "email": file_path.name
        }
        context.new_inbox_emails = email_list
        context.save()


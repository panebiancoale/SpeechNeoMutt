import os
import time
import pytest
import actions.email.general.reply_email as reply
from email.utils import formatdate, make_msgid
from pathlib import Path
from config import INBOX_DIR, HOSTNAME
from services.core import state,context
from parser.parser import parser_command
from email.message import EmailMessage
from unittest import mock
from actions.actions_executor import execute



class TestReplyEmail:
    """
    Classe di test per verificare il corretto funzionamento del modulo rispondi email
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

    def test_reply_email_success(self):
        """
        Test di successo per il modulo 'reply_email' con risposta solo al mittente
        :return:
        """
        sender = "bob@example.com"
        dest = ['tesi.neomutt@gmx.com']
        subject = "oggetto di prova"
        body = "testo di prova"

        email_to_read = self.create_tmp_email(sender, dest, subject, body)
        self.update_context(email_to_read)
        input_stt = parser_command("rispondi")
        state.pending_intent = input_stt.get("intent")
        state.slots = input_stt.get("slots")

        with mock.patch.object(reply,"_ask_mode",return_value=True),\
             mock.patch.object(reply,"confirm_input",return_value=True),\
             mock.patch.object(reply,"get_body",return_value="questa è una risposta di prova \n ciao"),\
             mock.patch.object(reply,"_confirm_and_reply",return_value=True) as confirm_and_reply:

            execute(input_stt,state,context)

            assert confirm_and_reply.called
            args,kwargs = confirm_and_reply.call_args
            dest,subject,reply_body = args[2],args[3],args[7]

            assert dest == [sender]
            assert subject in f"Re: {subject}"
            assert reply_body in "risposta di prova"

    def test_reply_email_failure(self,clean_state):
        """
        Test di fallimento per il modulo 'reply_email'
        :return:
        """
        input_stt = parser_command("rispondi")
        state.pending_intent = input_stt.get("intent")
        state.slots = input_stt.get("slots")

        with mock.patch("actions.email.general.reply_email.text_to_speech.text_to_speech") as fail_reply:
            execute(input_stt,state,context)

            assert fail_reply.called
            args,kwargs = fail_reply.call_args
            text = args[0]

            assert 'Non ci sono email a cui rispondere' in text


    @staticmethod
    def create_tmp_email(sender, dest, subject, body):
        """
        Crea file per l'email da rispondere
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

        filename = f"{int(time.time())}.{os.getpid()}.{HOSTNAME}:2,S"
        tmp_filepath = Path.home() / INBOX_DIR / "cur" / filename

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
        context.current_email = {
            "folder": file_path.parent.name,
            "email": file_path.name
        }
        context.save()
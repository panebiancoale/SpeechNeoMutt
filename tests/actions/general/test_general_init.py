import os
import time
from email import policy
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.parser import BytesParser
from email.utils import formatdate, make_msgid, parseaddr
from pathlib import Path

from actions.email.general import parse_body
from config import HOSTNAME, INBOX_DIR


class TestGeneralInit:
    """
    Classe per testare metodi di '__init__' in general
    """
    def test_parse_body(self):
        """
        Testa il corretto funzionamento per parsare il testo di un messaggio
        :return:
        """
        sender = "bob@example.com"
        dest = ["tesi.neomutt@gmx.com"]
        subject = "Oggetto di prova"

        html_body = """
            <html>
            <body>
                <h1>Test parser html</h1>
                <p>Caro lettore,</p>
                <h2>Questo è un test!</h2>
            </body>
            </html>
            """

        parsed_msg = self.create_tmp_email(sender, dest, subject, html_body)
        # Parsing body
        body_text = parse_body(parsed_msg)
        assert body_text == "Test parser html\nCaro lettore,\nQuesto è un test!"


    @staticmethod
    def create_tmp_email(sender, dest, subject, html_body):
        """
        Crea messaggio posta elettronica
        :param sender: mittente
        :param dest: destinatario/i
        :param subject: oggetto
        :param html_body: testo
        :return: il messaggio
        """
        msg = MIMEMultipart("alternative")
        msg["From"] = sender
        msg["To"] = ", ".join(dest)
        msg["Subject"] = subject

        msg.attach(MIMEText(html_body, "html"))

        raw_bytes = msg.as_bytes()
        parsed_msg = BytesParser(policy=policy.default).parsebytes(raw_bytes)
        return parsed_msg
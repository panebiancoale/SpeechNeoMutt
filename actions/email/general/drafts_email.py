import logging
import os
import time
from email.message import EmailMessage
from email.utils import formatdate
from pathlib import Path
from actions.email import confirm_input
from config import EMAIL_ACCOUNT, HOSTNAME, DRAFT_DIR
from services.core import text_to_speech


def ask_for_save_drafts_in_write(dest_list,subject,body):
    """
    Chiede per salvare la bozza nel modulo 'write_email'
    :param dest_list: destinatari
    :param subject: oggetto
    :param body: testo
    :return: True se la bozza è salvata correttamente
    """
    ask = confirm_input("Vuoi salvare la bozza?")
    if ask:
        logging.debug(f"Destinatario: {dest_list}")
        logging.debug(f"Subject: {subject}")
        logging.debug(f"Body: {body}")
        draft_file = _save_drafts_in_write(dest_list,subject,body)
        if draft_file:
            logging.debug(f"Bozza salvata: {draft_file.name}")
            text_to_speech.text_to_speech("Bozza salvata")
            return True
    return None

def ask_for_save_drafts_in_reply(original_date,sender,dest_list,subject,original_body,reply_body,add_original_body):
    """
    Chiede per salvare la bozza nel modulo 'reply_email'
    :param original_date: data dell'email originale
    :param sender: mittente originale
    :param dest_list: destinatari
    :param subject: oggetto
    :param original_body: testo email originale
    :param reply_body: testo email di risposta
    :param add_original_body: True se si vuole includere il testo originale
    :return: True se la bozza è salvata correttamente
    """
    ask = confirm_input("Vuoi salvare la bozza?")
    if ask:
        draft_file = _save_drafts_in_reply(original_date,sender,dest_list,subject,original_body,reply_body,add_original_body)
        if draft_file:
            logging.debug(f"Bozza salvata: {draft_file.name}")
            text_to_speech.text_to_speech("Bozza salvata")
            return True
    return None


def _save_drafts_in_write(dest_list,subject,body):
    """
    Salva la bozza nella directory DRAFT_DIR
    :param dest_list: destinatari
    :param subject: oggetto
    :param body: testo
    :return: il percorso del file
    """
    msg = EmailMessage()
    msg["Date"] = formatdate(localtime=True)
    msg["From"] = EMAIL_ACCOUNT
    msg["To"] = ",".join(dest_list)
    msg["Subject"] = subject
    msg.set_content(body)

    filename = f"{int(time.time())}.{os.getpid()}.{HOSTNAME}"
    tmp_file = Path.home() / DRAFT_DIR / "new" / filename

    with open(tmp_file,"wb") as f:
        f.write(msg.as_bytes())

    return tmp_file

def _save_drafts_in_reply(original_date,sender,dest_list,subject,original_body,reply_body,add_original_body):
    """
    Salva la bozza nella directory DRAFT_DIR
    :param original_date: data dell'email originale
    :param sender: mittente originale
    :param dest_list: destinatari
    :param subject: oggetto
    :param original_body: testo email originale
    :param reply_body: testo di risposta
    :param add_original_body: True se si vuole includere il testo originale
    :return: il percorso del file
    """
    msg = EmailMessage()
    msg["Date"] = formatdate(localtime=True)
    msg["From"] = EMAIL_ACCOUNT
    msg["To"] = ",".join(dest_list)
    msg["Subject"] = subject

    quoted_body = None
    if add_original_body:
        if original_body:
            lines = [line.strip() for line in original_body.strip().splitlines() if line.strip()]
            original_lines = [f"> {line}" for line in lines if line]
            quoted_lines = "\n".join(original_lines)
            quoted_body = f"On {original_date}, {sender} wrote:\n{quoted_lines}"

    email_msg = ""
    if quoted_body:
        email_msg += f"{quoted_body}\n\n"

    email_msg += f"{reply_body.strip()}\n"
    msg.set_content(email_msg)

    filename = f"{int(time.time())}.{os.getpid()}.{HOSTNAME}"
    tmp_file = Path.home() / DRAFT_DIR / "new" / filename

    with open(tmp_file,"wb") as f:
        f.write(msg.as_bytes())

    return tmp_file
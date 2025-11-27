import logging
from email import policy
from email.parser import BytesParser
from pathlib import Path

from actions.email import NUMBERS_TO_ORDINALS, NUMBERS_TO_WORDS
from config import INBOX_DIR
from email_client.backend_neomutt import get_emails_with_neomutt
from services.core import text_to_speech

def _get_new_emails():
    """
    Carica le nuove email in arrivo
    :return: la lista delle email
    """
    new_emails = []
    all_new_emails = get_emails_with_neomutt(Path.home()/INBOX_DIR/"new")
    for email in all_new_emails:
        if not ":2,S" in email["email"]:
            if not ":2,RS" in email["email"]:
                new_emails.append(email)

    return new_emails


def check_new_email(slots=None,context=None):
    """
    Controlla se ci sono nuove email in arrivo
    :param slots: non utilizzato
    :param context: contesto corrente
    :return: le nuove email in arrivo
    """
    new_emails = _get_new_emails()
    logging.debug(f"Email presenti: {new_emails}")

    if context:
        context.new_inbox_emails = new_emails
        context.save()

    total_new = len(new_emails)
    word_number = NUMBERS_TO_WORDS.get(total_new)

    if total_new == 0:
        text_to_speech.text_to_speech("Non ci sono nuove email.")
    else:
        if total_new == 1:
            start = "C'è"
            end = "nuova email"
        else:
            start = "Ci sono"
            end = "nuove email"
        text_to_speech.text_to_speech(f"{start} {word_number} {end}")
        working_list = new_emails.copy()
        _read_subject(working_list)

    return total_new

def _read_subject(email_list):
    """
    Legge gli oggetti delle nuove email
    :param email_list: lista delle email
    :return: Legge con il modulo TextToSpeech
    """
    for index,file_to_read in enumerate(email_list,start=1):
        folder = file_to_read["folder"]
        email =file_to_read["email"]

        file_path =  Path.home()/ INBOX_DIR / folder / email
        subject = _parse_subject(file_path)

        logging.debug(f"Oggetto: {subject}")
        ordinal_word = NUMBERS_TO_ORDINALS.get(index)

        if len(email_list) == 1:
            if subject:
                text_to_speech.text_to_speech(f"Ha come oggetto {subject}")
            else:
                text_to_speech.text_to_speech(f"Non ha oggetto")
        else:
            if subject:
                text_to_speech.text_to_speech(f"La {ordinal_word} email ha come oggetto {subject}")
            else:
                text_to_speech.text_to_speech(f"La {ordinal_word} email non ha oggetto")


def _parse_subject(file_path):
    """
    Parsa email per ottenere l'oggetto
    :param file_path: percorso del file che corrisponde all'email
    :return: Oggetto se presente
    """
    try:
        with open(file_path, "rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)

        subject = msg.get("Subject")
        return subject
    except Exception as e:
        logging.exception(f"Errore nel parsing {file_path}: {e}")
        return None

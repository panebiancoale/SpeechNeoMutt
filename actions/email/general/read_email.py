import logging
from email import policy
from email.parser import BytesParser
from email.utils import parseaddr
from pathlib import Path
from actions.action_cancelled import ActionCancelled
from actions.email.general import add_flags, ask_for_index, parse_body
from config import INBOX_DIR
from services.core import text_to_speech

def read_email(slots=None,context=None):
    """
    Gestisce la lettura delle email in arrivo
    :param slots: contiene variabili utili
    :param context: contesto corrente
    :return: Chiama la funzione per le leggere le email
    """
    try:
        slots = slots
        email_index = slots.get("index")

        if context.new_inbox_emails:
            _read_new_inbox(context,email_index)
        else:
            text_to_speech.text_to_speech("Non ci sono email da leggere")
            return None

    except ActionCancelled as ac:
        logging.exception(ac)
        return None

def read_again(slots=None,context=None):
    """
    Gestisce la lettura dell'ultima email letta
    :param slots:  non utilizzato
    :param context:  contesto corrente
    :return:  Chiama la funzione per le leggere le email
    """
    try:
        if not context.current_email:
            text_to_speech.text_to_speech("Non ci sono email da leggere")
            return None

        file_to_read = context.current_email
        email_path = Path.home()/ INBOX_DIR / file_to_read["folder"] / file_to_read["email"]
        if not email_path.exists():
            text_to_speech.text_to_speech("Nessuna email trovata")
            return None

        sender, subject, body = _parse_email(email_path)
        content = f"From: {sender}\nSubject: {subject}\n{body}"
        logging.debug(f"Email: {content}")

        text_to_speech.text_to_speech(f"Rileggo la email inviata da: {sender} oggetto {subject} {body}")

    except ActionCancelled as ac:
        logging.exception(ac)
        return None



def _read_new_inbox(context,email_index):
    """
    Gestisce la lettura delle nuove email in arrivo
    :param context: contesto corrente
    :param email_index: indice dell'email
    :return: chiama la funzione per le leggere le email
    """
    logging.debug(f"Legge le nuove email")
    working_list = context.new_inbox_emails.copy()
    logging.debug(f"Email presenti: {working_list}")
    _read(working_list,email_index,context)

def _read(email_list,email_index,context):
    """
    Si occupa di selezionare,e leggere l'email corretta
    :param email_list: lista delle email presenti
    :param email_index: indice dell'email
    :param context: contesto corrente
    :return: Legge l'email con il modulo TextToSpeech
    """
    if email_index is None:
        if len(email_list) == 1:
            email_index = 1
        else:
            email_index = ask_for_index(email_list, "Dimmi quale email leggere")
        if email_index is None:
            return None

    file_to_read = email_list[email_index - 1]
    folder = file_to_read["folder"]
    email = file_to_read["email"]
    email_folder = Path.home()/ INBOX_DIR / folder
    file_path = email_folder / email

    if not file_path.exists():
        text_to_speech.text_to_speech(f"Nessuna email trovata {email}.")
        return None

    sender, subject, body = _parse_email(file_path)
    content = f"From: {sender}\nSubject: {subject}\n{body}"
    logging.debug(f"Email: {content}")

    new_filepath = add_flags(file_path,"S")
    new_filepath = move_to_cur(new_filepath)
    file_to_read["email"] = new_filepath.name
    file_to_read["folder"] = new_filepath.parent.name
    _update_context(context,file_to_read)

    # Legge il contenuto ad alta voce
    text_to_speech.text_to_speech(f"Ecco la mail inviata da {sender}, oggetto {subject}, {body}")

    return None

def move_to_cur(file_path):
    """
    Sposta email da new/ a cur/
    :param file_path: percorso del file
    :return: il nuovo percorso del file
    """
    destination = Path.home()/ INBOX_DIR / "cur"
    new_path = destination / file_path.name
    file_path.rename(new_path)
    return new_path



def _parse_email(file_path):
    """
    Parsa email per ottenere mittente,oggetto,testo
    :param file_path: percorso del file che corrisponde all'email
    :return: Mittente, oggetto, testo
    """
    try:
        with open(file_path, "rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)

        sender = msg.get("From")
        name, addr = parseaddr(sender)
        sender = name or addr
        subject = msg.get("Subject")

        body = parse_body(msg)

        return sender, subject, body

    except Exception as e:
        logging.exception(f"Errore nel parsing {file_path}: {e}")
        return None


def _update_context(context,file_to_read):
    """
    Agggiorna lo stato interno
    :param context: contesto corrente
    :param file_to_read: file che corrisponde all'email
    :return: contesto aggiornato
    """
    if context is not None:
        context.current_email = file_to_read
        context.save()
        logging.debug(f"Aggiornato contesto {file_to_read}")
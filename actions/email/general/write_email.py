import logging
import os.path
import tempfile

from actions.action_cancelled import ActionCancelled
from actions.email import get_dest_list, get_subject, get_body, confirm_input
from actions.email.general import get_choice, get_modify_choice, handle_modify, resolve_addr
from actions.email.general.drafts_email import ask_for_save_drafts_in_write
from email_client.backend_neomutt import send_email_with_neomutt
from services.core import text_to_speech
from parser.parser import parser_command


def write_email(slots=None,context=None):
    """
    Gestisce la scrittura di una nuova email
    :param slots: contiene componenti riconosciuti dal parser
    :param context: non utilizzato
    :return: True se l'invio è riuscito
    """
    try:
        logging.debug("Scrive email")
        slots = slots
        dest_list = slots.get("dest")
        subject = slots.get("subject")
        body = slots.get("body")

        if not dest_list or any(dest is None for dest in dest_list):
            dest_list = get_dest_list()

        if not subject or subject is None:
            subject = get_subject()

        if not body or body is None:
            body = get_body()

        logging.debug(f"Destinatario: {dest_list}")
        logging.debug(f"Subject: {subject}")
        logging.debug(f"Body: {body}")

        return _confirm_and_send(dest_list, subject, body)

    except ActionCancelled as ac:
        logging.exception(ac)
        return None

def _confirm_and_send(dest_list, subject, body):
    """
    Chiede e riceve conferma per invio email
    :param dest_list: destinatario/i dell'email
    :param subject: oggetto dell'email
    :param body: testo dell'email
    :return: True se l'invio è riuscito
    """
    data = None
    while True:
        addr_list = resolve_addr(dest_list)
        result = confirm_input(f"Stai inviando a {', '.join(addr_list)} con oggetto {subject} testo {body}, confermi?")

        if result:
            tmp_write = _create_tmp_file_for_body(body)
            if send_email_with_neomutt(tmp_write,dest_list, subject):
                text_to_speech.text_to_speech("Email inviata")
                logging.debug(f"Destinatario: {dest_list}, Oggetto: {subject}, Testo: {body}")
                if os.path.exists(tmp_write):
                    os.remove(tmp_write)
                return True
        else:
            try:
                choice = get_choice()

                if choice.startswith("modifica"):
                    if "testo" in choice:
                        mod_text = "modifica testo"
                    elif choice in ["destinatario","destinatari"]:
                        mod_text = "modfica destinatario"
                    elif "oggetto" in choice:
                        mod_text = "modifica oggetto"
                    else:
                        mod_text = get_modify_choice()

                    data = parser_command(mod_text)

                dest_list, subject, body = handle_modify(data, dest_list, subject, body)
            except ActionCancelled:
                return ask_for_save_drafts_in_write(dest_list,subject,body)

def _create_tmp_file_for_body(body):
    """
    Crea file temporaneo per il testo del messaggio
    :param body: testo dell'email da scrivere nel file
    :return: il percorso del file
    """
    try:
        with tempfile.NamedTemporaryFile("w",delete=False,encoding="utf-8") as tmp_file:
            tmp_file.write(body)
            tmp_path = tmp_file.name

        return tmp_path
    except Exception as e:
        logging.exception(f"Errore nel creare il file temporaneo: {e}")
        return None
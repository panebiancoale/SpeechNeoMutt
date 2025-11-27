import logging
import os
import tempfile
from email import policy
from email.parser import BytesParser
from email.utils import getaddresses, parseaddr
from pathlib import Path
from actions.action_cancelled import ActionCancelled
from actions.email import get_body, confirm_input
from actions.email.general import get_choice, parse_body, resolve_addr
from actions.email.general import add_flags
from actions.email.general.drafts_email import ask_for_save_drafts_in_reply
from actions.email.modify.modify_body import modify_body
from config import INBOX_DIR, EMAIL_ACCOUNT
from email_client.backend_neomutt import reply_email_with_neomutt
from services.core import text_to_speech
from parser.parser import parser_command

"""
Il modulo reply è limitato dal comportamento di Neomutt che non supporta risposte
con invio 'automatico', di conseguenza non è implementabile senza uscire dal core del progetto,
in quanto richiederebbe una delle seguenti condizioni:
1. gestire il file temporaneo nella gui del client così da permettere l'invio della risposta
2. gestire l'invio della risposta con configurazione SMTP esterna a Neomutt 
"""


def reply_email(slots=None,context=None):
    """
    Gestisce la risposta ad una email
    :param slots: non utilizzato
    :param context: contesto corrente
    :return: True se la risposta è inviata
    """
    try:
        logging.debug("Risponde all'email")
        email_to_reply = context.current_email
        if not email_to_reply:
            text_to_speech.text_to_speech("Non ci sono email a cui rispondere")
            return None

        file_path = Path.home()/ INBOX_DIR / email_to_reply["folder"] / email_to_reply["email"]
        if not file_path.exists():
            text_to_speech.text_to_speech(f"Nessuna email trovata {email_to_reply['email']}")
            return None

        date_send,sender,to_list,subject,message_id,references,body = _parse_email(file_path)

        mode = _ask_mode()
        if mode:
            dest_list = [sender]
        else:
            dest_list = [sender] + to_list

        choice = confirm_input("Includo il messaggio nella risposta?")

        reply_body = get_body()

        # Aggiunge 'Re:' se non presente
        if not subject.lower().startswith("re"):
            subject = f"Re: {subject}"

        return _confirm_and_reply(date_send,sender,dest_list,subject,choice,message_id,references,reply_body,body,file_path,context)
    except ActionCancelled as ac:
        logging.exception(ac)
        return None


def _ask_mode():
    """
    Chiede la modalità di risposta
    :return: True se si risponde al mittente, false altrimenti
    """
    response = confirm_input("Vuoi rispondere solo al mittente?")
    logging.debug(f"Risposta {response}")
    return response

def _parse_email(file_path):
    """
    Parsa email per ottenere mittente e destinatari
    :param file_path: percorso del file che corrisponde all'email
    :return: mittente e destinatari
    """
    try:
        with open(file_path, "rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)

        date_send = msg.get("Date")
        sender = msg.get("From")
        name, addr = parseaddr(sender)
        sender = addr
        to_list = msg.get_all("To", [])
        subject = msg.get("Subject")
        message_id = msg.get("Message-ID")
        references = msg.get_all("References",[])
        if message_id:
            references = references + [message_id]

        to_list = [addr for name,addr in getaddresses(to_list)]

        body = parse_body(msg)

        return date_send,sender, to_list, subject, message_id, references, body

    except Exception as e:
        logging.exception(f"Errore nel parsing {file_path}: {e}")
        return None

def _create_tmp_reply(date_send,sender,dest_list,subject,message_id,references,reply_body,body,choice):
    """
    Crea file temporaneo per gestire correttamente la risposta con neomutt
    :param date_send: data di invio email originale
    :param sender: mittente originale
    :param dest_list: destinatari della risposta
    :param subject: oggetto originale
    :param message_id: message id originale
    :param references: references ai messaggi precedenti
    :param reply_body: testo di risposta
    :param body: testo originale
    :param choice: True se si include il testo originale
    :return: il path del file temporaneo
    """
    try:
        if not subject.lower().startswith("re"):
            subject = f"Re: {subject}"

        original_body = None
        if choice:
            if body:
                lines = [line.strip() for line in body.strip().splitlines() if line.strip()]
                original_lines = [f"> {line}" for line in lines if line]
                quoted_lines = "\n".join(original_lines)
                original_body = f"On {date_send}, {sender} wrote:\n{quoted_lines}"


        headers = [
            f"From: {EMAIL_ACCOUNT}",
            f"To: {', '.join(dest_list)}",
            f"Subject: {subject}"
        ]
        if message_id:
            headers.append(f"In-Reply-To: {message_id}")
        if references:
            headers.append(f"References: {', '.join(references)}")
        headers.append(f"Content-Type: text/plain; charset=utf-8")

        headers.append("\n")

        email_msg = "\n".join(headers)
        if original_body:
            email_msg += f"{original_body}\n\n"

        email_msg += f"{reply_body.strip()}\n"

        with tempfile.NamedTemporaryFile("w",delete=False,encoding="utf-8") as tmp_file:
            tmp_file.write(email_msg)
            tmp_path = tmp_file.name

        return tmp_path
    except Exception as e:
        logging.exception(f"Errore nel creare il file temporaneo per la risposta: {e}")
        return None

def _create_tmp_file_for_body(date_send,sender,original_body,reply_body,choice):
    """
    Crea file temporaneo per il testo del messaggio
    :param date_send: data messaggio originale
    :param sender: mittente originale
    :param original_body: testo originale
    :param reply_body: testo di risposta
    :param choice: True se si include il testo originale
    :return: il persorso del file temporaneo
    """
    try:
        quoted_body = None
        if choice:
            if original_body:
                lines = [line.strip() for line in original_body.strip().splitlines() if line.strip()]
                original_lines = [f"> {line}" for line in lines if line]
                quoted_lines = "\n".join(original_lines)
                quoted_body = f"On {date_send}, {sender} wrote:\n{quoted_lines}"

        email_msg = ""
        if quoted_body:
            email_msg += f"{quoted_body}\n\n"

        email_msg += f"{reply_body.strip()}\n"

        with tempfile.NamedTemporaryFile("w",delete=False,encoding="utf-8") as tmp_file:
            tmp_file.write(email_msg)
            tmp_path = tmp_file.name

        return tmp_path
    except Exception as e:
        logging.exception(f"Errore nel creare il file temporaneo per il testo della risposta: {e}")
        return None


def _confirm_and_reply(date_send,sender,dest_list,subject,with_original_body,message_id,references,reply_body,body,file_path,context):
    """
    Chiede e riceve conferma per inviare risposta
    :param date_send: data di invio email originale
    :param sender: mittente
    :param dest_list: destinatari
    :param subject: oggetto
    :param with_original_body: True se si include il testo originale
    :param message_id: message_id (NON UTILIZZATO)
    :param references: riferimenti alle email a cui si risponde (NON UTILIZZATO)
    :param reply_body: testo della risposta
    :param body: testo della email originale
    :param file_path: percorso del file da rispondere
    :param context: contesto corrente
    :return: True se la risposta è inviata
    """
    mod_text = None
    while True:
        addr_list = resolve_addr(dest_list)
        result = confirm_input(f"Stai rispondendo a {', '.join(addr_list if addr_list else dest_list)} con oggetto {subject} testo {reply_body} confermi?")

        if result:
            tmp_reply = _create_tmp_file_for_body(date_send,sender,body,reply_body,with_original_body)
            if reply_email_with_neomutt(tmp_reply,dest_list,subject):
                new_file_path = add_flags(file_path,"R")
                file_dict = {
                    "folder": "cur",
                    "email": new_file_path.name
                }

                _update_context(context,file_dict)
                text_to_speech.text_to_speech("Risposta inviata")
                logging.debug(f"Destinatario: {dest_list}, Testo: {reply_body}")
                if os.path.exists(tmp_reply):
                    os.remove(tmp_reply)
                return True
        else:
            try:
                choice = get_choice()
                if choice.startswith("modifica"):
                    mod_text = "modifica testo"

                data = parser_command(mod_text)
                intent = data.get("intent")
                if intent == "modify_body":
                    reply_body = modify_body(reply_body)
            except ActionCancelled:
                return ask_for_save_drafts_in_reply(date_send,sender,dest_list,subject,body,reply_body,with_original_body)

def _update_context(context,file_to_reply):
    """
    Agggiorna lo stato interno
    :param context: contesto corrente
    :param file_to_reply: file che corrisponde all'email
    :return: contesto aggiornato
    """
    if context is not None:
        base = file_to_reply["email"].split(":2")[0]

        context.new_inbox_emails = [
            email for email in context.new_inbox_emails if email["email"].split(":2")[0] != base
        ]

        context.current_email = file_to_reply
        context.save()
        logging.debug(f"Aggiornato contesto {file_to_reply}")

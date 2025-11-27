import logging
from actions.email.modify import replace_word,delete_word
from actions.email import get_subject, ask_user_or_stop, confirm_input
from actions.email.modify.add_subject import add_subject
from parser.parser import parser_command

def modify_subject(current_subject):
    """
    Modifica oggetto dell'email
    :param current_subject: oggetto corrente
    :return: il nuovo oggetto
    """
    logging.debug("Modifica l'oggetto dell'email")
    while True:
        text = ask_user_or_stop("Specifica l'operazione")
        logging.info("Pronuncia 'esci', 'chiudi' oppure 'stop' per terminare")

        if text in ("esci","chiudi","stop"):
            break

        data = parser_command(text)
        intent = data.get("intent")
        slots= data.get("slots")
        if intent == "replace_word":
            current_subject = replace_word(current_subject,slots)
        elif intent == "rewrite":
            current_subject = _get_subject()
        elif intent == "add":
            current_subject = add_subject(current_subject,slots)
        elif intent == "delete_word":
            current_subject = delete_word(current_subject,slots)
        else:
            continue

        current_subject = current_subject
        logging.debug(f"Oggetto corrente: {current_subject}")

    return current_subject

def _get_subject():
    """
    Chiede conferma del testo ricevuto
    :return: il soggetto
    """
    while True:
        subject = get_subject()
        conf = confirm_input(f"Ho capito {subject}, confermi?")
        if conf:
            return subject
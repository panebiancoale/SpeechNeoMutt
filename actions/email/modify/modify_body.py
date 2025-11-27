import logging
from actions.email.modify import replace_word, delete_word
from actions.email.modify.add_body import add_body
from parser.parser import parser_command
from actions.email import get_body, ask_user_or_stop, confirm_input


def modify_body(current_body):
    """
    Modifica il testo dell'email
    :param current_body: testo corrente
    :return: il nuovo testo
    """
    logging.debug("Modifica il testo dell'email")
    while True:
        text = ask_user_or_stop("Specifica l'operazione")
        logging.info("Pronuncia 'esci', 'chiudi' oppure 'stop' per terminare")

        if text in ("esci","chiudi","stop"):
            break

        data = parser_command(text)
        intent = data.get("intent")
        slots = data.get("slots")
        if intent == "replace_word":
            current_body = replace_word(current_body,slots)
        elif intent == "rewrite":
            current_body = _get_body()
        elif intent == "add":
            current_body = add_body(current_body,slots)
        elif intent == "delete_word":
            current_body = delete_word(current_body,slots)
        else:
            continue

        current_body = current_body
        logging.debug(f"Testo corrente: {current_body}")

    return current_body


def _get_body():
    """
    Chiede conferma del testo ricevuto
    :return: il testo
    """
    while True:
        body = get_body()
        conf = confirm_input(f"Ho capito {body}, confermi?")
        if conf:
            return body
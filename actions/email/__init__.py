import logging
import re

from actions.action_cancelled import ActionCancelled
from config import ALIAS_TO_ADDR
from services.core import text_to_speech,state,speech_to_text
from state.dialogue_state import DialoguePhase

ORDINALS = {
    "prima": 1, "seconda": 2, "terza": 3, "quarta": 4,
    "quinta": 5, "sesta": 6, "settima": 7, "ottava": 8,
    "nona": 9, "decima": 10, "undicesima": 11, "dodicesima": 12,
    "tredicesima": 13, "quattordicesima": 14, "quindicesima": 15,
    "sedicesima": 16, "diciasettesima": 17, "diciottesima": 18,
    "diciannovesima": 19, "ventesima": 20,
    "uno": 1, "due": 2, "tre": 3, "quattro": 4, "cinque": 5,
    "sei": 6, "sette": 7, "otto": 8, "nove": 9, "dieci": 10,
    "undice": 11, "dodici": 12, "tredici": 13, "quattordici": 14,
    "quindici": 15, "sedici": 16, "diciasette": 17, "diciotto": 18,
    "diciannove": 19, "venti": 20
}

NUMBERS_TO_ORDINALS = {
    1:"prima",2:"seconda",3:"terza",4:"quarta",5:"quinta",6:"sesta",7:"settima",
    8:"ottava",9:"nona",10:"decima",11:"undicesima",12:"dodicesima",13:"tredicesima",
    14:"quattordicesima",15:"quindicesima",16:"sedicesima",17:"diciasettesima",
    18:"diciottesima",19:"diciannovesima",20:"ventesima"
}

NUMBERS_TO_WORDS = {
    1:"una",2:"due",3:"tre",4:"quattro",5:"cinque",6:"sei",7:"sette",
    8:"otto",9:"nove",10:"dieci", 11:"undici", 12:"dodici", 13:"tredici",
    14:"quattordici", 15:"quindici", 16:"sedici", 17:"diciasette", 18:"diciotto",
    19:"diciannove", 20:"venti"
}

PUNCTUATION = {
    "virgola":",", "punto semplice":".", "punto di domanda":"?", "punto esclamativo":"!"
}

ACTIONS_IN_EDIT_TEST = {
    "a capo":"\n", "nuova linea":"\n"
}

def resolve_alias(dest):
    """
    Restituisce indirizzo in contatti
    :param dest:
    :return:
    """
    return ALIAS_TO_ADDR.get(dest.lower())

def parse_dest(dest):
    """
    Supporta destinatari multipli divisi da 'e'
    :param dest:
    :return:
    """
    parts = re.split(r"\s*(?:,|\be\b)\s*",dest.strip())
    parts = [x.strip() for x in parts if x.strip()]
    return parts

def confirm_input(text):
    """
    Chiede conferma con il testo passato
    :param text:
    :return:
    """
    response = ask_user_or_stop(text)
    logging.debug(f"Conferma {response}")
    if response in ["si","sì","se","conferma","confermo"]:
        return True
    elif response in ["no"]:
        return False
    else:
        return confirm_input(text)

def get_dest_list():
    """
    Chiede e restituisce i destinatari per l'email
    :return:
    """
    dest_list = []
    while not dest_list:
        dest_input = ask_user_or_stop("A chi la invio?")
        for dest in parse_dest(dest_input):
            real = resolve_alias(dest)
            if real:
                dest_list.append(real)
        if not dest_list:
            text_to_speech.text_to_speech("Contatto non trovato")

    confirm = confirm_input(f"Ho capito {', '.join(dest_list)}, confermi?")
    if not confirm:
        return get_dest_list()
    return dest_list

def get_subject():
    """
    Chiede e restituisce l'oggetto dell'email
    :return:
    """
    subject = ask_user_or_stop("Dimmi l'oggetto")
    return subject

def get_body():
    """
    Chiede e restituisce il testo dell'email
    :return:
    """
    body = ask_user_or_stop("Dimmi il testo")
    for key,value in PUNCTUATION.items():
        body = body.replace(key,value)
        body = body.replace(f" {value}",value)
    for key,value in ACTIONS_IN_EDIT_TEST.items():
        body = body.replace(key,value)
        body = body.replace(f"{value} ",value)
    return body


def ask_user_or_stop(text):
    """
    Chiede all'utente il testo, supportando annulla che interrompe l'azione
    :param text:
    :return:
    """
    response = ask_user(text)
    if response is None:
        text_to_speech.text_to_speech("Non ho capito")
        return ask_user_or_stop(text)

    response = response.lower()
    logging.debug(f"Risposta {response}")
    if response in ["annulla","a nulla","annullare"]:
        state.set_phase(DialoguePhase.IDLE)
        raise ActionCancelled("Azione annulata")

    return response

def ask_user(text,retry_msg = "Puoi ripetere",retries = 2):
    """
    Chiede all'utente il testo, con un numero massimo di tentativi
    :param text:
    :param retry_msg:
    :param retries:
    :return:
    """
    for attempt in range(retries+1):
        text_to_speech.text_to_speech(text)

        response = speech_to_text.speech_to_text()
        if response:
            return response
        else:
            text_to_speech.text_to_speech(retry_msg)

    return None
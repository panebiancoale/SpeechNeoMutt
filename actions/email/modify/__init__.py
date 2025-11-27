import logging

from actions.email import ask_user_or_stop, confirm_input, PUNCTUATION
from services.core import text_to_speech

def ask_word(text):
    """
    Chiede il testo specificato
    :param text: testo
    :return: la risposta dell'utente
    """
    response = ask_user_or_stop(text)
    return response

def replace_word(current_text,slots):
    """
    Sostituisce la parola specificata con una nuova
    :param current_text: testo corrente
    :param slots: contiene la parola da sostituire e la nuova
    :return:
    """
    word_to_replace = slots.get("word_to_replace")
    new_word = slots.get("new_word")
    if not word_to_replace:
        word_to_replace = _get_word("Dimmi quale parola vuoi sostituire")
    if not new_word:
        new_word = _get_word("Dimmi la nuova parola")

    if word_to_replace in PUNCTUATION.keys():
        word_to_replace = PUNCTUATION.get(word_to_replace)
    if new_word in PUNCTUATION.keys():
        new_word = PUNCTUATION.get(new_word)

    while True:
        if word_to_replace not in current_text:
            logging.debug(f"Parola {word_to_replace} non presente nel testo")
            word_to_replace = ask_word("Dimmi quale parola vuoi sostituire")
            continue
        else:
            break

    new_text = current_text.replace(word_to_replace,new_word)
    if new_word in PUNCTUATION.values():
        new_text = new_text.replace(f" {new_word}",f"{new_word}")

    logging.debug(f"{word_to_replace} SOSTITUITA CON {new_word}")
    text_to_speech.text_to_speech("Parola sostituita correttamente")
    return new_text

def _get_word(text):
    """
    Chiede conferma della parola ricevuta
    :param text: il testo da chiedere
    :return: la parola
    """
    while True:
        word = ask_word(text)
        if word:
            conf = confirm_input(f"Ho capito {word}, confermi?")
            if conf:
                return word
            else:
                continue


def delete_word(current_text,slots):
    """
    Elimina la parola specificata dal testo
    :param current_text: testo corrente
    :param slots: contiene la parola da eliminare
    :return:
    """
    word_to_delete = slots.get("word_to_delete")
    if not word_to_delete:
        word_to_delete = _get_word("Dimmi quale parola")

    if word_to_delete in PUNCTUATION.keys():
        word_to_delete = PUNCTUATION.get(word_to_delete)

    while True:
        if word_to_delete not in current_text:
            logging.debug(f"Parola {word_to_delete} non presente nel testo")
            word_to_delete = ask_word("Dimmi quale parola vuoi eliminare")
            continue
        else:
            break

    new_text = current_text.replace(word_to_delete,"")
    text_to_speech.text_to_speech("Parola eliminata correttamente")
    return new_text


def add_word_after(current_text, word_limit, new_part):
    """
    Aggiunge la nuova parte nel testo corrente dopo la parola specificata
    :param current_text: testo corrente
    :param word_limit: parola specificata
    :param new_part: nuova parte del testo
    :return: il nuovo testo
    """
    if not word_limit:
        word_limit = _get_word("Dimmi quale parola")

    if word_limit in PUNCTUATION.keys():
        word_limit = PUNCTUATION.get(word_limit)

    position = current_text.find(word_limit)

    if position != -1:
        if all(char in PUNCTUATION.values() for char in new_part):
            new_text = current_text[:position + len(word_limit)] + new_part + current_text[position + len(word_limit):]
        else:
            new_text = current_text[:position + len(word_limit)] + " " + new_part + current_text[position + len(word_limit):]
        return new_text

    return current_text

def add_word_before(current_text, word_limit, new_part):
    """
     Aggiunge la nuova parte nel testo corrente prima la parola specificata
    :param current_text: testo corrente
    :param word_limit: parola specificata
    :param new_part: nuova parte del testo
    :return: il nuovo testo
    """
    if not word_limit:
        word_limit = _get_word("Dimmi quale parola")

    if word_limit in PUNCTUATION.keys():
        word_limit = PUNCTUATION.get(word_limit)

    position = current_text.find(word_limit)

    if position != -1:
        if position == 0:
            new_text = current_text[:position] + new_part + " " + current_text[position:]
        else:
            new_text = current_text[:position] + " " + new_part + current_text[position:]
        return new_text

    return current_text
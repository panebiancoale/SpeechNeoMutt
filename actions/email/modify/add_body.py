import logging
from actions.email import get_body, confirm_input, PUNCTUATION
from actions.email.modify import add_word_after, add_word_before


def add_body(current_body,slots):
    """
    Aggiunge al testo già presente
    :param current_body: testo attuale
    :param slots: contiene la posizione
    :return: il nuovo testo
    """
    logging.debug("Aggiunge al testo già presente")
    while True:
        new_body_part = get_body()
        position = slots.get("position")
        word_limit = slots.get("word_limit")

        if position == "start":
            new_body = f"{new_body_part} {current_body}"
        elif position == "after":
            new_body = add_word_after(current_body,word_limit,new_body_part)
        elif position == "before":
            new_body = add_word_before(current_body,word_limit,new_body_part)
        else:
            if any(char in PUNCTUATION.values() for char in new_body_part):
                new_body = f"{current_body}{new_body_part}"
            else:
                new_body = f"{current_body} {new_body_part}"

        conf = confirm_input(f"Nuovo testo {new_body}, confermi?")
        if conf:
            return new_body

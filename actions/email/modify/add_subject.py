import logging
from actions.email import get_subject, confirm_input
from actions.email.modify import add_word_after, add_word_before


def add_subject(current_subject,slots):
    """
    Aggiunge all'oggetto già presente
    :param current_subject: oggetto attuale
    :param slots: contiene la posizione
    :return: l'oggetto nuovo
    """
    logging.debug("Aggiunge all'oggetto presente")
    while True:
        new_subject_part = get_subject()
        position = slots.get("position")
        word_limit = slots.get("word_limit")

        if position == "before":
            new_subject = add_word_before(current_subject, word_limit, new_subject_part)
        elif position == "after":
            new_subject = add_word_after(current_subject, word_limit, new_subject_part)
        elif position == "start":
            new_subject = f"{new_subject_part} {current_subject}"
        else:
            new_subject = f"{current_subject} {new_subject_part}"

        conf = confirm_input(f"Nuovo oggetto {new_subject}, confermi?")
        if conf:
            return new_subject

import logging

from actions.email import get_dest_list, confirm_input
from config import ADDR_TO_ALIAS


def add_dest(current_dest):
    """
    Aggiunge destinatario/i a quello/i già presenti
    :param current_dest: destinatario/i attuale/i
    :return: la lista con i/il destinatario/destinatario
    """
    logging.debug("Aggiunge destinatario/i")
    while True:
        new_dest_list = get_dest_list()
        new_dest_list.extend(current_dest)
        if len(new_dest_list) == 1:
            start = "Nuovo destinatario"
        else:
            start = "Nuovi destinatari"

        addr = ADDR_TO_ALIAS(new_dest_list)
        conf = confirm_input(f"{start} {', '.join(addr)}, confermi?")
        if conf:
            return new_dest_list

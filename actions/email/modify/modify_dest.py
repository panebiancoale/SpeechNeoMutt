import logging

from actions.email import get_dest_list, confirm_input
from config import ADDR_TO_ALIAS


def modify_dest():
    """
    Modifica destinatario/i della email
    :return: la lista con i/il destinatari/destinatario
    """
    logging.debug("Modifica destinatario/i della email")
    while True:
        new_dest_list = get_dest_list()
        if len(new_dest_list) == 1:
            start = "Nuovo destinatario"
        else:
            start = "Nuovi destinatari"

        addr = ADDR_TO_ALIAS(new_dest_list)
        conf = confirm_input(f"{start} {', '.join(addr)}, confermi?")
        if conf:
            return new_dest_list


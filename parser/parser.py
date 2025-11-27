from .clear_text import clear_text
from .find_intent import find_intent
from .find_slots import find_slots



def parser_command(text):
    """
    Elabora il testo per riconoscere l'intent, associato all'azione corretta
    :param text: testo riconosciuto dal modulo STT
    :return: dizionario con 'intent' e 'slots'
    """
    tokens = clear_text(text)
    intent = find_intent(tokens)
    slots = find_slots(text,intent)

    return {"intent":intent,"slots":slots}
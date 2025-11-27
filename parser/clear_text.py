import re

def clear_text(text):
    """
    Pulisce il testo di input
    :param text:  testo da elaborare
    :return: il testo corretto
    """
    text = text.lower().strip()
    # \b confine tra parola e un carattere "speciale" (spazio,punteggiatura...)
    # [\w']+ gruppo di uno o più caratteri (a-z and ')
    return re.findall(r"\b[\w']+\b", text)
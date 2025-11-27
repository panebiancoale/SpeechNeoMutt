import shutil
from services.core import text_to_speech
def is_neomutt_installed() -> bool:
    """
    Controllo se neomutt è installato
    :return: true se neomutt è installato
    """
    return shutil.which("neomutt") is not None

def assert_neomutt():
    """
    Se neomutt non è installato, fornisce feedback e chiude il programma
    :return:
    """
    if not is_neomutt_installed():
        text_to_speech.text_to_speech("Neomutt non installato")
        exit(1)
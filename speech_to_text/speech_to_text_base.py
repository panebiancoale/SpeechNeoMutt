from abc import ABC, abstractmethod

class SpeechToTextBase(ABC):
    """
    Classe Astratta per SpeechToText.
    """

    @abstractmethod
    def speech_to_text(self) -> str:
        """
        Restituisce il testo riconosciuto
        :return: testo riconosciuto
        """
        pass
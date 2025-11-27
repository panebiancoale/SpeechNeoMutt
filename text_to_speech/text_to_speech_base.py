from abc import ABC, abstractmethod

class TextToSpeechBase(ABC):
    """
    Classe Astratta per TextToSpeech.
    """

    @abstractmethod
    def text_to_speech(self, text: str):
        """
        Ritorna il testo in modalità vocale
        :param text:
        :return: testo vocale
        """
        pass
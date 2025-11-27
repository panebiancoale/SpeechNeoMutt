import json
import threading

import vosk
import pyaudio
import numpy as np
from scipy.signal import resample_poly
from .email_dictionary import dictionary_json
from .speech_to_text_base import SpeechToTextBase
from config import *

FRAME_PER_BUFFER = 8192

class SpeechToTextVosk(SpeechToTextBase):
    def __init__(self, model_path = VOSK_MODEL_PATH, device_rate=DEVICE_RATE):
        self.device_rate = device_rate
        self.model = vosk.Model(model_path)
        self.recognizer = vosk.KaldiRecognizer(self.model, TARGET_RATE,dictionary_json)

        #Inizializzo stream
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.device_rate,
            input=True,
            frames_per_buffer=FRAME_PER_BUFFER
        )
        self.barge_in_event = threading.Event()
        self._listening = False
        self._callback = None



    def resample_chunk(self, chunk:bytes) -> bytes:
        """
        Resemple audio
        :param chunk:
        :return:
        """
        audio_np = np.frombuffer(chunk, dtype=np.int16)
        audio_resampled = resample_poly(audio_np, TARGET_RATE,self.device_rate)
        return audio_resampled.astype(np.int16).tobytes()

    def speech_to_text(self,callback= None):
        """
        Cattura input vocale dell'utente
        :param callback: funzione per utilizzare barge-in
        :return: testo riconosciuto
        """
        if callback:
            self._callback = callback
            self._listening = True
            threading.Thread(target=self._loop_listen,daemon=True).start()
            return None
        else:
            while True:
                data = self.stream.read(FRAME_PER_BUFFER, exception_on_overflow=False)
                if self.device_rate != TARGET_RATE:
                    data = self.resample_chunk(data)

                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").strip()
                    if text:
                        return text


    def _loop_listen(self):
        """
        Loop per rilevare barge-in
        :return:
        """
        while self._listening:
            data = self.stream.read(FRAME_PER_BUFFER,exception_on_overflow=False)
            if self.device_rate != TARGET_RATE:
                data = self.resample_chunk(data)
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                text = result.get("text","").strip()
                if text:
                    self.barge_in_event.set()
                    if self._callback:
                        self._callback(text)

    def stop_barge_in(self):
        """
        Ferma il thread asincrono
        :return:
        """
        self.barge_in_event.clear()
        self._listening = False
        self._callback = None

    def close(self):
        """
        Chiude risore audio
        :return:
        """
        self.stop_barge_in()
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
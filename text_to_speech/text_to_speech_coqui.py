import logging

import numpy as np
import pyaudio
import threading
import queue
from scipy.signal import resample_poly
from TTS.api import TTS
from config import COQUI_MODEL, DEVICE_RATE, COQUI_RATE
from text_to_speech.text_to_speech_base import TextToSpeechBase

class TextToSpeechCoqui(TextToSpeechBase):
    def __init__(self, model_name=COQUI_MODEL, coqui_rate=COQUI_RATE):
        self.tts = TTS(model_name)
        self.target_rate = DEVICE_RATE
        self.p = pyaudio.PyAudio()
        self.coqui_rate = coqui_rate
        self.queue = queue.Queue()
        self._stop_event = threading.Event()
        self._current_thread = threading.Thread(target=self._current, daemon=True)
        self._current_thread.start()


    def _current(self):
        """
        Prende elemento dalla coda e lo riproduce
        :return:
        """
        while True:
            text = self.queue.get()
            if text is None:
                break
            self._stop_event.clear()
            try:
                self._play_audio(text)
            except Exception as e:
                logging.exception(f"Errore in TTS: {e}")

    def _play_audio(self, text):
        """
        Riproduce il testo
        :param text: il testo da riprodurre
        :return:
        """
        audio = np.array(self.tts.tts(text=text))

        # Resampling da 16kHz a 44.1KHz
        if self.target_rate != self.coqui_rate:
            up = self.target_rate // np.gcd(self.target_rate, self.coqui_rate)
            down = self.coqui_rate // np.gcd(self.target_rate, self.coqui_rate)
            audio = resample_poly(audio, up, down)

        # Normalizza in [-1,1]
        if np.max(np.abs(audio)) > 0:
            audio = audio / np.max(np.abs(audio))

        # Converte in int16
        audio_int16 = (audio * 32767).astype(np.int16)
        stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.target_rate,
            output=True
        )

        for i in range(0,len(audio_int16),512):
            if self._stop_event.is_set():
                break
            stream.write(audio_int16[i:i+512].tobytes())

        stream.stop_stream()
        stream.close()


    def text_to_speech(self, text: str):
        """
        Popola la coda
        :param text: il testo da inserire in coda
        :return:
        """
        self.queue.put(text)

    def stop(self):
        """Ferma immediatamente la riproduzione"""
        self._stop_event.set()

    def is_playing(self):
        """
        Verifia se è attivo
        :return:
        """
        return not self.queue.empty() or not self._stop_event.is_set()

    def close(self):
        """
        Chiude le risorse
        :return:
        """
        self.stop()
        self.queue.put(None)
        if self._current_thread.is_alive():
            self._current_thread.join(timeout=1)
        self.p.terminate()

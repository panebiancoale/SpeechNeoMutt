import threading

from config import USE_VOSK
from state.dialogue_context import DialogueContext
from state.dialogue_state import DialogueState
from text_to_speech.text_to_speech_coqui import TextToSpeechCoqui
from speech_to_text.speech_to_text_vosk import SpeechToTextVosk

text_to_speech = TextToSpeechCoqui()
if USE_VOSK:
    speech_to_text = SpeechToTextVosk()

state = DialogueState()
context = DialogueContext()

stop_event = threading.Event()
import logging
from actions.actions_executor import execute
from config import CHECK_NEOMUTT, USE_VOSK
from email_client.check_neomutt import assert_neomutt
from services.core import speech_to_text,state,context,stop_event,text_to_speech
from parser.parser import parser_command
from state.dialogue_state import DialoguePhase

def barge_in_on(text):
    """
    Callback chiamata dal modulo STT
    :param text: testo intercettato
    :return:
    """
    logging.info(f"[INFO] Trascrizione: {text}")
    if text_to_speech.is_playing():
        logging.info("[INFO] Stop TTS...")
        text_to_speech.stop()

    data = parser_command(text)
    logging.info(f"[INFO] Intent: {data}")

    state.pending_intent = data.get("intent")
    state.slots = data.get("slots",{})


    execute(data,state,context)

    if state.phase == DialoguePhase.IDLE:
        state.reset()
        context.save()


def director():
    """
    Gestione del flusso principale ascolta (SpeechToText) e parla (TextToSpeech)
    :return:
    """
    logging.basicConfig(level=logging.DEBUG, format="%(name)s - %(levelname)s - %(message)s")
    if CHECK_NEOMUTT:
        assert_neomutt()


    logging.info("Assistente vocale attivo")

    try:
        if USE_VOSK:
        # Resta attivo finché non arriva uno stop
            speech_to_text.speech_to_text(callback=barge_in_on)
            stop_event.wait()
    except KeyboardInterrupt:
        logging.info("Interrotto da tastiera")
        stop_event.set()
    finally:
        logging.info("Chiusura...")
        context.clean()
        speech_to_text.close()
        text_to_speech.close()
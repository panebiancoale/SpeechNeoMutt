from actions.email.general.check_new_email import check_new_email
from actions.email.general.read_email import read_email, read_again
from actions.email.general.reply_email import reply_email
from actions.email.general.write_email import write_email
from state.dialogue_state import DialoguePhase

INTENT_MAP = {
    "write_email":(write_email,DialoguePhase.WRITING),
    "read_email":(read_email,DialoguePhase.READING),
    "notify_new_inbox": (check_new_email,DialoguePhase.NOTIFY),
    "reply_email":(reply_email,DialoguePhase.REPLYING),
    "read_again": (read_again,DialoguePhase.READING)
}

def execute(data,state,context):
    """
    Esegue le azioni riconosciute dal parser e che sono nella mappa degli intent
    :param data: dizionario con 'intent' e 'slots'
    :param state: stato corrente
    :param context: contesto corrente
    :return: chiama la funzione associata all'intento
    """
    intent = data.get("intent")
    slots= data.get("slots",{})
    if not intent or intent not in INTENT_MAP:
        state.set_phase(DialoguePhase.IDLE)
        return None

    func,phase = INTENT_MAP[intent]
    state.set_phase(phase)
    return func(slots,context)
from enum import Enum,auto

class DialoguePhase(Enum):
    IDLE = auto()
    READING = auto()
    WRITING = auto()
    NOTIFY = auto()
    REPLYING = auto()

class DialogueState:
    """
    Tiene traccia dello stato corrente
    """
    def __init__(self):
        self.phase = DialoguePhase.IDLE
        self.pending_intent = False
        self.slots = {}

    def set_phase(self, phase: DialoguePhase):
        self.phase = phase

    def reset(self):
        self.phase = DialoguePhase.IDLE
        self.pending_intent = False
        self.slots = {}
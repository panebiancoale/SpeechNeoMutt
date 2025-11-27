import re
from actions.email import ORDINALS, resolve_alias


def find_slots(text,intent):
    """
    Cerca gli slots presenti nel testo
    :param text:  testo da elaborare
    :param intent: intento riconosciuto
    :return: gli slots corretti se riconosciuti
    """
    slots = {}

    # Scrivi email
    if intent == "write_email":
        dest_match = re.search(r"\ba\s+(?P<dest>.+?)(?=\s+con\b|\s+oggetto|\s+testo\b|$)",text)
        if dest_match:
            # divide destinatari multipli
            dest = re.split(r"\s*(?:,|\be\b)\s*",dest_match.group("dest").strip())
            slots["dest"] = [resolve_alias(d) for d in dest if d]

        subject_match = re.search(r"(?:\bcon\s+)?\boggetto\b\s+(?P<subject>.+?)(?=\s+testo\b|$)",text)
        if subject_match:
            slots["subject"] = subject_match.group("subject").strip()

        body_match = re.search(r"\btesto\b\s+(?P<body>.+?)$",text)
        if body_match:
            slots["body"] = body_match.group("body").strip()

    # Leggi email
    elif intent == "read_email":
        number_match = re.search(r"numero\s+(\w+)",text)
        ordinal_match = re.search(r"^leggi\s+(?:la\s+)?(\w+)",text)
        candidate = (number_match or ordinal_match)
        if candidate:
            word = candidate.group(1)
            index = ORDINALS.get(word)
            if index:
                slots["index"] = index

    # Aggiungi al testo corrente
    elif intent == "add":
        match_after = re.search(r"\s+dopo(?:\s+(?:(il|la)\s+)?(?P<word>\w+))?", text)
        match_before = re.search(r"\s+prima(?:\s+(?:di|del|della)\s*(?P<word>\w+))?", text)
        if re.search(r"\balla fine\b",text):
            slots["position"] = "end"
        elif re.search(r"\ball'inizio\b",text):
            slots["position"] = "start"
        elif match_after:
            slots["word_limit"]= match_after.group("word").strip() if match_after.group("word") else None
            slots["position"] = "after"
        elif match_before:
            slots["word_limit"]= match_before.group("word").strip() if match_before.group("word") else None
            slots["position"] = "before"
        else:
            slots["position"] = "end"

    # Sostituisci parola
    elif intent == "replace_word":
        word_match = re.search(r"\s+(?:(il|la)\s+)?(?P<word_to_replace>\w+)",text)
        if word_match:
            slots["word_to_replace"] = word_match.group("word_to_replace").strip()
        new_word_match = re.search("con\s+(?:(il|la)\s+)?(?P<new_word>[\w\s]+)",text)
        if new_word_match:
           slots["new_word"] = new_word_match.group("new_word").strip() if new_word_match.group("new_word") else None

    # Cancella parola
    elif intent == "delete_word":
        word_match = re.search(r"\s+(?:il|la)?(?P<word_to_delete>[\w\s]+)$",text)
        if word_match:
            slots["word_to_delete"] = word_match.group("word_to_delete").strip()


    return slots

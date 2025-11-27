def find_intent(tokens):
    """
    Riconosce l'intento principale
    :param tokens: testo da elaborare
    :return: l'intento se riconosciuto altrimenti 'unknown'
    """

    if "scrivi" in tokens:
        return "write_email"

    if "leggi" in tokens:
        return "read_email"

    if "rispondi" in tokens:
        return "reply_email"

    if any(token in ["novità","nuove"] for token in tokens):
        return "notify_new_inbox"

    if "modifica" in tokens:
        if "destinatario" in tokens or "destinatari" in tokens:
            return "modify_dest"
        if "oggetto" in tokens:
            return "modify_subject"
        if "testo" in tokens:
            return "modify_body"


    if "aggiungi" in tokens:
        if "destinatario" in tokens or "destinatari" in tokens:
            return "add_dest"
        else:
            return "add"


    if "rileggi" in tokens:
        return "read_again"

    if "sostituisci" in tokens:
        return "replace_word"

    if "cambia" in tokens:
        return "rewrite"

    if "cancella" in tokens:
        return "delete_word"

    return "unknown"
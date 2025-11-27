import logging
import re
from bs4 import BeautifulSoup
from actions.email import ask_user_or_stop, ORDINALS
from config import ADDR_TO_ALIAS

ORDER_FLAGS = "DRFTS" # ordine dei flag nel formato maildir
def add_flags(file_path,flags):
    """
    Aggiunge i flag 'S' 'R' al nome del file
    :param file_path: percorso del file
    :param flags: flag da aggiungere
    :return: percorso del file
    """
    filename = file_path.name

    if ":2" in filename:
        base, curr_flags = filename.split(":2,",1)
    else:
        base, curr_flags = filename,""

    new_flags_set = set(curr_flags) | set(flags)
    new_flags = "".join(f for f in ORDER_FLAGS if f in  new_flags_set)

    new_filename = f"{base}:2,{new_flags}"

    if new_filename == filename:
        return file_path

    new_path = file_path.with_name(new_filename)
    file_path.rename(new_path)
    return new_path


def ask_for_index(email_list,text):
    """
    Chiede quale email selezionare
    :param email_list: lista delle email presenti
    :param text: testo da chiedere
    :return: indice dell'email
    """
    response = ask_user_or_stop(text)
    logging.debug(f"Risposta: {response}")
    index = extract_index(response)
    if 1 < index < len(email_list):
        return index
    else:
        return None

def extract_index(response):
    """
    Estrae l'indice corretto dell'email
    :param response: testo che contiene l'indice dell'email
    :return: indice dell'email
    """
    match = re.search(r"(?:numero\s)+(\w+)",response)
    if match:
        number = match.group(1)
        return ORDINALS.get(number)

    match = re.search(r"(?:la\s)+(\w+)",response)
    if match:
        ordinal = match.group(1)
        return ORDINALS.get(ordinal)

    return None

def get_choice():
    """
    Chiede se si vuole modificare (cambiare) o aggiungere (integrare ciò che è già presente)
    :return: la scelta
    """
    choice = ask_user_or_stop("Vuoi modificare o annullare?")
    choice = choice.lower()
    logging.debug(f"Scelta {choice}")
    if choice.startswith("modifica"):
        return choice
    else:
        return get_choice()

def get_modify_choice():
    """
    Chiede e riceve ciò che si vuole modificare
    :return: la scelta
    """
    mod_text = ask_user_or_stop("Cosa vuoi modificare?")
    mod_text = mod_text.lower()
    logging.debug(f"Scelta {mod_text}")
    if not mod_text.startswith("modifica"):
        if mod_text in ["testo","oggetto","destinatario","destinatari"]:
            mod_text = f"modifica {mod_text}"
        else:
            return get_modify_choice()

    return mod_text


def get_add_choice():
    """
    Chiede e riceve ciò che si vuole aggiungere
    :return: la scelta
    """
    add_text = ask_user_or_stop("Cosa vuoi aggiungere?")
    add_text = add_text.lower()
    logging.debug(f"Scelta {add_text}")
    if not add_text.startswith("aggiungi"):
        if add_text in ["testo","testo all'inizio","testo alla fine","oggetto","oggetto all'inizio","oggetto alla fine","destinatario","destinatari"]:
            add_text = f"aggiungi {add_text}"
        else:
            return get_add_choice()

    return add_text


def handle_modify(data, dest_list, subject, body):
    """
    Gestisce la modifica e l'aggiunta con le azioni corrette
    :param data: contiene 'intent' e 'slots' se presenti
    :param dest_list: destinatario/i presenti
    :param subject: oggetto presente
    :param body: testo presente
    :return: i campi aggiornati
    """
    from actions.email.modify.modify_dest import modify_dest
    from actions.email.modify.modify_subject import modify_subject
    from actions.email.modify.modify_body import modify_body
    intent = data.get("intent")
    if intent == "modify_dest":
        dest_list = modify_dest()
    elif intent == "modify_subject":
        subject = modify_subject(subject)
    elif intent == "modify_body":
        body = modify_body(body)

    return dest_list, subject, body

def resolve_addr(address):
    """
    Cerca l'alias corretto per l'indirizzo email
    :param address: indirizzo email
    :return: singolo alias o lista di alias a seconda dell'input
    """
    if isinstance(address, str):
        return ADDR_TO_ALIAS.get(address)
    elif isinstance(address,list):
        addr_list = []
        for addr in address:
            resolved_addr = resolve_addr(addr)
            if resolved_addr:
                addr_list.append(resolved_addr)

        return addr_list
    else:
        return None

def parse_body(msg):
    """
    Parsa il testo dell'email
    :param msg: il messaggio di posta elettronica
    :return: il testo
    """
    plain_body = None
    html_body = None
    for part in msg.walk():
        content_type = part.get_content_type()
        disposition = str(part.get_content_disposition() or "")
        if disposition == "attachment":
            continue  # ignora allegati

        if content_type == "text/plain" and plain_body is None:
            plain_body = part.get_content()
        elif content_type == "text/html" and html_body is None:
            html_body = part.get_content()

    if plain_body:
        return plain_body

    if html_body:
        return _html_to_plain_text(html_body)

    return ""



def _html_to_plain_text(html_body):
    """
    Converte html to plain text
    :param html_body: testo html dell'email
    :return: teto in formato plain
    """
    soup = BeautifulSoup(html_body, "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    for tag in soup.find_all(["p", "li", "h1", "h2", "h3", "h4", "h5", "h6"]):
        tag.insert_after("\n")

    text = soup.get_text(separator="\n",strip=True)
    return "\n".join(line for line in text.splitlines() if line.strip())


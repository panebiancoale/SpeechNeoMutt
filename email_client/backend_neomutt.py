import logging
import os
import subprocess

from config import ACCOUNT_SYNC

def _sync_folder():
    try:
        subprocess.run(["mbsync","-a",ACCOUNT_SYNC],check=True)
        logging.debug("Sincronizza Maildir")
    except subprocess.CalledProcessError as e:
        logging.exception(f"Errore nella sincronizzazione Maildir {e}")

def send_email_with_neomutt(file_path,dest_list, subject):
    """
    Invio email
    :param file_path: percorso del file contenente il testo del messaggio
    :param dest_list: destinatario/i
    :param subject: oggetto
    :return: True se l'invio è riuscito
    """
    try:
        env = os.environ.copy()
        env["PATH"] += ":/usr/bin"

        # -s <subject> IMPOSTA L'OGGETTO
        # -- SEPARA LE OPZIONI DAI DEST
        # *dest_list ESPANDE LA LISTA DEI DEST
        cmd = ["/usr/bin/neomutt","-s",subject, "--", *dest_list]

        with open(file_path,"r") as file:
            subprocess.run(
                cmd,
                input=file.read().encode("utf-8"),
                check=True,
                env=env
            )

        _sync_folder()

        return True
    except subprocess.CalledProcessError as e:
        logging.exception(f"Errore nell'invio dell'email {e}")
        return False

"""
def reply_email_with_neomutt(file_path):
    Risposta email
    :param file_path: percorso al file da rispondere
    :return: True se l'invio è riuscito
    try:
        env = os.environ.copy()
        env["PATH"] += ":/usr/bin"

        # -H <file> SELEZIONA IL FILE DA COMPLETARE
        cmd = ["/usr/bin/neomutt","-E","-H",file_path,"-B"]
        subprocess.run(cmd, check=True, env=env)

        _sync_folder()
        return True
    except subprocess.CalledProcessError as e:
        logging.exception(f"Errore nella risposta dell'email {e}")
        return False
"""
def reply_email_with_neomutt(file_path, dest_list, subject):
    """
    Risposta email
    :param file_path: percorso del file
    :param dest_list: destinatario/i
    :param subject: oggetto
    :return: True se la risposta è stata inviata correttamente
    """
    try:
        env = os.environ.copy()
        env["PATH"] += ":/usr/bin"

        cmd = ["/usr/bin/neomutt","-s",subject, "--", *dest_list]
        with open(file_path,"r") as file:
            subprocess.run(
                cmd,
                input=file.read().encode("utf-8"),
                check=True,
                env=env
            )

        _sync_folder()
        return True
    except subprocess.CalledProcessError as e:
        logging.exception(f"Errore nella risposta dell'email {e}")
        return False



def get_emails_with_neomutt(email_folder=None):
    """
    Recupera email dalla cartella specificata
    :param email_folder:  cartella
    :return: lista di email
    """
    _sync_folder()
    email_list = []
    for folder in [email_folder]:
        if folder.exists():
            for f in folder.iterdir():
                if f.is_file():
                    email_list.append({
                        "folder": folder.name,
                        "email": f.name
                    })

    return email_list



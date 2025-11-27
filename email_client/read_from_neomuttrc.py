import logging
import re
from pathlib import Path

def load_from_neomuttrc():
    """
    Legge il file di configurazione di neomutt, per ricavare le informazioni necessarie come:
        - inbox_dir, sent_dir, drafts_dir
        - account, alias
    :return:
    """
    folder,inbox_dir,sent_dir,account = None,None,None,None
    alias_to_addr = {}
    try:
        path = Path.home() / ".neomuttrc"
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("set"):
                    if "folder" in line:
                        match = re.search(r'set\s+folder\s*=\s*"?([^"]+)"?', line)
                        if match:
                            folder = match.group(1).replace("~/","")
                    if "spoolfile" in line:
                        match = re.search(r'set\s+spoolfile\s*=\s*"?([^"]+)"?', line)
                        if match:
                            inbox_dir = match.group(1).replace("+","").replace('"',"")
                    if "record" in line:
                        match = re.search(r'set\s+record\s*=\s*"?([^"]+)"?', line)
                        if match:
                            sent_dir = match.group(1).replace("+","").replace('"',"")
                    if "postponed" in line:
                        match = re.search(r'set\s+postponed\s*=\s*"?([^"]+)"?', line)
                        if match:
                            draft_dir = match.group(1).replace("+","").replace('"',"")
                    if "from" in line:
                        match = re.search(r'set\s+from\s*=\s*"?([^"]+)"?', line)
                        if match:
                            account = match.group(1)
                    if "hostname" in line:
                        match = re.search(r'set\s+hostname\s*=\s*"?([^"]+)"?', line)
                        if match:
                            hostname = match.group(1)
                elif line.startswith("alias"):
                    match = re.search(r'alias\s+(\S+)\s*(?:=\s*)?("?)([^"\s]+)\2',line)
                    if match:
                        name = match.group(1).lower()
                        addr = match.group(3)
                        alias_to_addr[name] = addr

        addr_to_alias = {val: key for key, val in alias_to_addr.items()}
        if not folder:
            folder = "Mail"

        return folder,sent_dir,inbox_dir,account,alias_to_addr,addr_to_alias,draft_dir,hostname
    except FileNotFoundError as e:
        logging.exception(f"Errore nella lettura file {e}")

#Frequenza sample
TARGET_RATE = 16000
DEVICE_RATE = 44100
COQUI_RATE = 22050

#Percorso modello Vosk
VOSK_MODEL_PATH = "./model/vosk-model-it-0.22"

#Modello CoquiTTS
COQUI_MODEL = "tts_models/it/mai_male/glow-tts"

#Percorso per context storage
CONTEXT_PATH = "./state/context.json"

CHECK_NEOMUTT = True

#Uso modello Vosk per STT
USE_VOSK = True

# Account da sincronizzare con mbsync
ACCOUNT_SYNC = "gmx"

from email_client.read_from_neomuttrc import load_from_neomuttrc
folder,sent_dir,inbox_dir,account,alias_to_addr,addr_to_alias,draft_dir,hostname = load_from_neomuttrc()

#Directory Reali
INBOX_DIR = f"{folder}/{inbox_dir}"
SENT_DIR = f"{folder}/{sent_dir}"
DRAFT_DIR = f"{folder}/{draft_dir}"

#Directory per test
#from tests.actions.test_config import load_for_test
#inbox_test_dir, draft_test_dir, sent_test_dir = load_for_test()
#INBOX_DIR = inbox_test_dir
#DRAFT_DIR = draft_test_dir
#SENT_DIR = sent_test_dir

#Email account
EMAIL_ACCOUNT = account

#Hostname
HOSTNAME = hostname

#Contatti
ALIAS_TO_ADDR = alias_to_addr
ADDR_TO_ALIAS = addr_to_alias

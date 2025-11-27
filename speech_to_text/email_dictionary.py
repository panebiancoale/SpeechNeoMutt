import json

email_dictionary = [
    # **** Comandi generali ****
    "scrivi", "scrivi a",
    "invia",
    "leggi", "leggi la","rileggi", "rileggi ultima","rileggi ultima email che hai letto", "rileggi ultima email",
    "rispondi",
    "annullare", "annulla",
    "modificare",
    "chiudi", "stop", "esci",
    "elimina","cancella",
    "inbox", "arrivate", "in entrata", "in arrivo",
    "outbox","bozze","bozza",
    "in uscita","sent","inviate",
    "novità","nuove",
    "email","e-mail","mail",
    "spostata","rinviata",
    "riunione di",
    "elimina email",
    "archivia","archivia email",
    "ci sono nuove", "controlla nuove",
    "aggiornamenti","aggiornamento",
                                             
    # **** Oggetto ****
    "oggetto","riunione","informazioni",
    
    # **** Testo ****
    "testo","grazie","cordiali saluti",
    
    # **** Date ****
    "oggi","domani","mattina","pomeriggio","settimana",
    "lunedì","martedì","mercoledì","giovedì","venerdì","sabato","domenica",
    
    # **** Specifiche ****
    "chiocciola","punto","gmail","outlook","yahoo","azienda","it","com","trattino","underscore"
]

dictionary_json = json.dumps(email_dictionary,ensure_ascii=False,indent=2)
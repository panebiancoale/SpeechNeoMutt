# SpeechNeoMutt
Progetto per Tesi Triennale Informatica

**In questo progetto si è lavorato per sviluppare un interfaccia vocale da integrare poi con il client NeoMutt.**

Il software è stato sviluppato e testato su Linux e per poter  funzionare correttamente bisogna:

1. Configurare ambiente virtuale python Miniconda/Conda 
2. Installare le librerie python mancanti (se presenti)
3. Installare NeoMutt e aver configurato il file .neomuttrc
4. Installare mbsync e avere configurato il file .mbsyncrc (questo passaggio è necessario se si vuole avere la cartella locale sincronizzata con il server di posta elettronico)

**Esempio file .neomuttrc (contiene gli elementi richiesti dal software)**

```
#Maildir
set mbox_type = Maildir

#Directory
set folder = "~/Mail"
set spoolfile = +INBOX
set record = "+Sent"
set postponed = "+Drafts"
set send_charset="utf-8"

#IMAP
set imap_user = "il_tuo_account@email"
set set imap_pass = "la_tua_password"

set realname="il_tuo_realname"
set from="il_tuo_account@email"
set hostname="il_tuo_hostname"

#SMTP
set smtp_url="smtps://il_tuo_account@il_tuo_smtp:465/
set smtp_pass="la_tua_password"

#Alias
alias Me = "il_tuo_account@email"
```

**Esempio file .mbsyncrc** 

```
IMAPAccount il_tuo_provider
Host imap.il_tuo_provider
User il_tuo_account@email
Pass la_tua_password
SSLType IMAPS
AuthMechs LOGIN

IMAPStore il_tuo_provider-remote
Account account_imap

MaildirStore il_tuo_provider-local
Path ~/Mail/
Inbox ~/Mail/INBOX

Channel account_imap
Far :il_tuo_provider-remote:
Near :il_tuo_provider-local:
Patterns "INBOX" "Sent"
Create Near
SyncState *
```

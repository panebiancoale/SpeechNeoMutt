from unittest import mock
from email_client.read_from_neomuttrc import load_from_neomuttrc


class TestReadFromNeomuttrc:
    """
    Classe per verificare il corretto funzionamento del modulo leggi da file di configurazione neomutt
    """
    def test_read_from_neomuttrc(self,tmp_path):
        """
        Test per verificare se il file di configurazione di neomutt è parsato correttamente
        :param tmp_path: file temporaneo di pytest
        :return:
        """
        tmp_file = tmp_path / ".neomuttrc"
        tmp_file.write_text('''
        set folder = Mail
        set spoolfile = +INBOX
        set record = Sent
        set postponed = Draft
        set from = me@example.com
        set hostname = Neomutt
        alias Bob "bob@example.com"
        alias Tom "tom@example.com"
        ''')

        with mock.patch("pathlib.Path.home", return_value=tmp_path):
            folder, sent_dir, inbox_dir, account, alias_to_addr, addr_to_alias,draft_dir,hostname = load_from_neomuttrc()

            # Verifiche
            assert folder == "Mail"
            assert sent_dir == "Sent"
            assert inbox_dir == "INBOX"
            assert draft_dir == "Draft"
            assert account == "me@example.com"
            assert hostname == "Neomutt"
            assert alias_to_addr == {"bob":"bob@example.com","tom":"tom@example.com"}
            assert addr_to_alias == {"bob@example.com":"bob","tom@example.com":"tom"}
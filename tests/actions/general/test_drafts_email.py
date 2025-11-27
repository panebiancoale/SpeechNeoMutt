from unittest import mock
from actions.email.general.drafts_email import ask_for_save_drafts_in_write
import actions.email.general.drafts_email as drafts

class TestDraftsEmail:
    """
    Classe per testare i metodi del modulo 'drafts_email'
    """
    def test_drafts_email_in_write(self):
        """
        Testa il salvataggio della bozza partendo dal modulo 'write_email'
        :return:
        """
        dest = ['bob@example.com']
        subject = 'Test'
        body = 'Salvataggio bozza'

        with mock.patch("actions.email.ask_user_or_stop",return_value="si"),\
             mock.patch.object(drafts,"_save_drafts_in_write"),\
             mock.patch("actions.email.general.drafts_email.text_to_speech.text_to_speech") as stt:
            assert ask_for_save_drafts_in_write(dest,subject,body)
            args,kwargs = stt.call_args
            assert args[0] == "Bozza salvata"





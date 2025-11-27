import json
from pathlib import Path
from config import CONTEXT_PATH


class DialogueContext:
    """
    Contesto che tiene traccia delle email sulla quale si lavora
    """
    def __init__(self,storage_path = CONTEXT_PATH):
        self.storage_path = Path(storage_path)
        self.current_email: str | None = None
        self.new_inbox_emails: list[str] = []

        self._load()

    def _load(self):
        if self.storage_path.exists():
            try:
                data = json.loads(self.storage_path.read_text())
                self.current_email = data.get("current_email")
                self.new_inbox_emails = data.get("new_inbox_emails")
            except RuntimeError as e:
                pass

    def save(self):
        data = {
            "current_email": self.current_email,
            "new_inbox_emails": self.new_inbox_emails,
        }
        self.storage_path.write_text(json.dumps(data,indent=2))

    def clean(self):
        data = {
            "current_email": None,
            "new_inbox_emails":[],
        }
        self.storage_path.write_text(json.dumps(data,indent=2))


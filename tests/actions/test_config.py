from pathlib import Path


def load_for_test():
    inbox_dir = "Mail_Test/Inbox"
    tmp_inbox_dir = Path.home() / inbox_dir
    (tmp_inbox_dir / "new").mkdir(parents=True, exist_ok=True)
    (tmp_inbox_dir / "cur").mkdir(parents=True, exist_ok=True)
    (tmp_inbox_dir / "tmp").mkdir(parents=True, exist_ok=True)

    drafts_dir = "Mail_Test/Drafts"
    tmp_drafts_dir = Path.home() / drafts_dir
    (tmp_drafts_dir / "new").mkdir(parents=True, exist_ok=True)
    (tmp_drafts_dir / "cur").mkdir(parents=True, exist_ok=True)
    (tmp_drafts_dir / "tmp").mkdir(parents=True, exist_ok=True)

    sent_dir = "Mail_Test/Sent"
    tmp_sent_dir = Path.home() / sent_dir
    (tmp_sent_dir / "new").mkdir(parents=True, exist_ok=True)
    (tmp_sent_dir / "cur").mkdir(parents=True, exist_ok=True)
    (tmp_sent_dir / "tmp").mkdir(parents=True, exist_ok=True)

    return inbox_dir, drafts_dir, sent_dir
from datetime import datetime

class Commit:
    id: int

    def __init__(self, href: str, date: datetime, message: str, commit_owner: str):
        id = None
        self.href = href
        self.date = date
        self.message = message
        self.commit_owner = commit_owner

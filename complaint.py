from datetime import datetime
from reply import Reply

class Complaint:
    reply: Reply
    rating: int

    def __init__(self, href: str, complained_item: str, title: str, date: datetime, view_count: int, like_count: int, complain_owner: str):
        self.href = href
        self.complained_item = complained_item
        self.title = title
        self.date = date
        self.view_count = view_count
        self.like_count = like_count
        self.complain_owner = complain_owner
        self.rating = None
        self.sovled = False
        self.commits = []
        self.replies = []

        
    def set_reply(self, date: str, message: str, score: str, replier: str):
        self.reply = Reply(date, message, score, replier)

    def set_reply(self, reply: Reply):
        self.reply = reply
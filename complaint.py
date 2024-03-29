from datetime import datetime
from reply import Reply

class Complaint:
    id: int
    reply: Reply
    rating: int

    def __init__(self, href: str, complained_item_id: int, title: str, date: datetime, view_count: int, like_count: int, member_id: int, rating: int, solved: bool):
        self.href = href
        self.complained_item_id = complained_item_id
        self.title = title
        self.date = date
        self.view_count = view_count
        self.like_count = like_count
        self.member_id = member_id
        self.rating = rating
        self.sovled = solved
        self.commits = []
        self.replies = []

        
    def set_reply(self, date: str, message: str, score: str, replier: str):
        self.reply = Reply(date, message, score, replier)

    def set_reply(self, reply: Reply):
        self.reply = reply
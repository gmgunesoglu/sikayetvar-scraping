from reply import Reply

class Complaint:
    reply: Reply

    def __init__(self, title: str, description: str, date: str, view_count: str, complainer: str):
        self.title = title
        self.description = description
        self.date = date
        self.view_count = view_count
        self.complainer = complainer
        self.reply = None
        
    def set_reply(self, date: str, message: str, score: str, replier: str):
        self.reply = Reply(date, message, score, replier)

    def set_reply(self, reply: Reply):
        self.reply = reply
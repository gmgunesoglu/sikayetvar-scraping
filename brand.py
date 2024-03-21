class Brand:
    def __init__(self, href: str, name: str, replied_complaint: int, total_complaint: int, average_reply_sec: int, rating_count: int, rating: int):
        self.href = href
        self.name = name
        self.replied_complaint = replied_complaint
        self.total_complaint = total_complaint
        self.average_reply_sec = average_reply_sec
        self.rating_count = rating_count
        self.rating = rating
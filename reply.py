from datetime import datetime

class Reply:
    id: int

    def __init__(self, href: str, message: str, date: datetime, is_from_brand: bool):
        self.id = None
        self.href = href
        self.message = message
        self.date = date
        self.is_from_brand = is_from_brand

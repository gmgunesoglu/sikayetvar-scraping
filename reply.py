from datetime import datetime

class Reply:
    id: int

    def __init__(self, complaint_id: int, message: str, date: datetime, is_from_brand: bool):
        self.id = None
        self.complaint_id = complaint_id
        self.message = message
        self.date = date
        self.is_from_brand = is_from_brand

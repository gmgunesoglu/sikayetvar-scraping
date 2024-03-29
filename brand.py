from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Brand(Base):
    __tablename__ = 'brand'

    id = Column(Integer, primary_key=True)
    href = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    replied_complaint = Column(Integer, nullable=False)
    total_complaint = Column(Integer, nullable=False)
    average_reply_sec = Column(Integer, nullable=False)
    rating_count = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)

    def __init__(self, href: str, name: str, replied_complaint: int, total_complaint: int, average_reply_sec: int, rating_count: int, rating: int):
        self.href = href
        self.name = name
        self.replied_complaint = replied_complaint
        self.total_complaint = total_complaint
        self.average_reply_sec = average_reply_sec
        self.rating_count = rating_count
        self.rating = rating
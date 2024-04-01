from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from reply import Reply

Base = declarative_base()

class Complaint(Base):
    __tablename__ = 'complaint'

    id = Column(Integer, primary_key=True)
    href = Column(String(255), nullable=False, unique=True)
    complained_item_id = Column(Integer, ForeignKey('complained_item.id'), nullable=False)
    title = Column(String(255), nullable=False)
    date = Column(DateTime, nullable=False)
    view_count = Column(Integer, nullable=False)
    like_count = Column(Integer, nullable=False)   
    member_id = Column(Integer, ForeignKey('member.id'), nullable=False)   
    rating = Column(Integer, nullable=True)
    solved = Column(Boolean, nullable=False)

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

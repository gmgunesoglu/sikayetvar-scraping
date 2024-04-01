from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Reply(Base):
    __tablename__ = 'reply'

    id = Column(Integer, primary_key=True)
    complaint_id = Column(Integer, ForeignKey('complaint.id'), nullable=False)   
    message = Column(String(255), nullable=False)
    date = Column(DateTime, nullable=False)
    is_from_brand = Column(Boolean, nullable=False)

    def __init__(self, complaint_id: int, message: str, date: datetime, is_from_brand: bool):
        self.id = None
        self.complaint_id = complaint_id
        self.message = message
        self.date = date
        self.is_from_brand = is_from_brand

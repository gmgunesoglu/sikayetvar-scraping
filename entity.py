from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Brand(Base):
    __tablename__ = 'brand'

    id = Column(Integer, primary_key=True)
    href = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    replied_complaint = Column(Integer, nullable=False)
    total_complaint = Column(Integer, nullable=False)
    average_reply_sec = Column(Integer, nullable=False)
    rating_count = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)

    complained_items = relationship("ComplainedItem", back_populates="brand")
    # complained_items: Mapped[List["ComplainedItem"]] = relationship(back_populates='brand')

    def __init__(self, href: str, name: str, replied_complaint: int, total_complaint: int, average_reply_sec: int, rating_count: int, rating: int):
        self.href = href
        self.name = name
        self.replied_complaint = replied_complaint
        self.total_complaint = total_complaint
        self.average_reply_sec = average_reply_sec
        self.rating_count = rating_count
        self.rating = rating


class ComplainedItem(Base):
    __tablename__ = 'complained_item'

    id = Column(Integer, primary_key=True)
    href = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    rating = Column(Integer, nullable=False)
    rating_count = Column(Integer, nullable=False)
    upper_item_id = Column(Integer, ForeignKey('complained_item.id'), nullable=True)
    brand_id = Column(Integer, ForeignKey('brand.id'), nullable=False)
    is_leaf = Column(Boolean, nullable=False)

    brand = relationship("Brand", back_populates="complained_items")
    # brand: Mapped["Brand"] = relationship(back_populates='complained_items')
    complaints = relationship("Complaint", back_populates="complained_items")
    
    def __init__(self, href: str, name: str, rating: int, rating_count: int, upper_item_id: int, brand_id: int):
        self.href = href
        self.name = name
        self.rating = rating
        self.rating_count = rating_count
        self.upper_item_id = upper_item_id
        self.brand_id = brand_id
        self.is_leaf = True

class Member(Base):
    __tablename__ = 'member'

    id = Column(Integer, primary_key=True)
    href = Column(String(255), nullable=False, unique=True)
  
    complaints = relationship("Complaint", back_populates="member")    

    def __init__(self, href: str):
        self.href = href

class Complaint(Base):
    __tablename__ = 'complaint'

    id = Column(Integer, primary_key=True)
    href = Column(String(255), nullable=False, unique=True)
    complained_item_id = Column(Integer, ForeignKey('complained_item.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False)
    view_count = Column(Integer, nullable=False)
    like_count = Column(Integer, nullable=False)   
    member_id = Column(Integer, ForeignKey('member.id'), nullable=False)   
    rating = Column(Integer, nullable=True)
    solved = Column(Boolean, nullable=False)

    complained_items = relationship("ComplainedItem", back_populates="complaints")
    member = relationship("Member", back_populates="complaints")
    replies = relationship("Reply", back_populates="complaint")

    def __init__(self, href: str, complained_item_id: int, title: str, description: str, date: datetime, view_count: int, like_count: int, member_id: int, rating: int, solved: bool):
        self.href = href
        self.complained_item_id = complained_item_id
        self.title = title
        self.description = description
        self.date = date
        self.view_count = view_count
        self.like_count = like_count
        self.member_id = member_id
        self.rating = rating
        self.solved = solved

class Reply(Base):
    __tablename__ = 'reply'

    id = Column(Integer, primary_key=True)
    complaint_id = Column(Integer, ForeignKey('complaint.id'), nullable=False)   
    message = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False)
    is_from_brand = Column(Boolean, nullable=False)

    complaint = relationship("Complaint", back_populates="replies")

    def __init__(self, complaint_id: int, message: str, date: datetime, is_from_brand: bool):
        self.id = None
        self.complaint_id = complaint_id
        self.message = message
        self.date = date
        self.is_from_brand = is_from_brand

class ErrorLog(Base):
    __tablename__ = 'error_log'

    id = Column(Integer, primary_key=True)
    message = Column(String(255), nullable=False)
    date = Column(DateTime, nullable=False)

    def __init__(self, message: str):
        self.message = message
        self.date = datetime.now()
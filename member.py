from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Member(Base):
    __tablename__ = 'member'

    id = Column(Integer, primary_key=True)
    href = Column(String(255), nullable=False, unique=True)
  
    def __init__(self, href: str):
        self.href = href
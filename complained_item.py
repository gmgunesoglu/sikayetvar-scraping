from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ComplainedItem(Base):
    __tablename__ = 'complained_item'

    id = Column(Integer, primary_key=True)
    href = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    rating = Column(Integer, nullable=False)
    rating_count = Column(Integer, nullable=False)
    upper_item_id = Column(Integer, ForeignKey('complained_item.id'), nullable=True)
    brand_id = Column(Integer, ForeignKey('brand.id'), nullable=False)

    brand = relationship("Brand", back_populates="complained_items")
    
    def __init__(self, href: str, name: str, rating: int, rating_count: int, upper_item_id: int, brand_id: int):
        self.href = href
        self.name = name
        self.rating = rating
        self.rating_count = rating_count
        self.upper_item_id = upper_item_id
        self.brand_id = brand_id
        self.is_leaf = True
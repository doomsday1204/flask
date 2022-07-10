from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from models.base_class import Base


class Product(Base):
    id = Column(Integer, autoincrement=True, index=True, primary_key=True, unique=True)
    asin = Column(String)
    create_date = Column(DateTime, default=func.now())
    title = Column(String)
    children = relationship("Review")



from sqlalchemy import Column, String, DateTime, Integer, func, ForeignKey

from models.base_class import Base


class Review(Base):
    id = Column(Integer, autoincrement=True, index=True, primary_key=True, unique=True)
    asin = Column(String)
    create_date = Column(DateTime, default=func.now())
    title = Column(String)
    text = Column(String(length=10000))
    parent_id = Column(Integer, ForeignKey("product.id"))

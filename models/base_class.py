from typing import Any

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import as_declarative, declared_attr

db = SQLAlchemy()

@as_declarative()
class Base:
    id: Any
    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

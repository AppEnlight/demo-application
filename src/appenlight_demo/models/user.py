from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
)

from sqlalchemy.orm import (
    relationship
)

from .meta import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode)
    addresses = relationship('Address')

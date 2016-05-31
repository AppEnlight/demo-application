from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    ForeignKey
)

from .meta import Base


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    address = Column(Unicode)
    phone = Column(Unicode)
    owner_id = Column(Integer, ForeignKey('users.id'))

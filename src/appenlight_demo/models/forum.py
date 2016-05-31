from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    ForeignKey
)

from .meta import Base


class Forum(Base):
    __tablename__ = 'forums'
    id = Column(Integer, primary_key=True)
    forum = Column(Unicode)

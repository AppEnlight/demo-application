from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    ForeignKey
)

from .meta import Base


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    forum_id = Column(Integer)
    post = Column(Unicode)

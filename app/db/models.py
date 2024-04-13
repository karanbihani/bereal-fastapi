from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    image_url_front = Column(String, nullable=False)
    image_url_back = Column(String, nullable=False)
    description = Column(String)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    location = Column(String, nullable = False, server_default = "NULL")
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    deleted = Column(Boolean, server_default="FALSE", nullable = False )
    deleted_at = Column(TIMESTAMP(timezone=True))
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    fullname = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    bio = Column(String,nullable=True)

class Reaction(Base):
    __tablename__ = "reactions"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"),primary_key=True)
    reaction_type = Column(Integer, nullable=False) # 1 is thumbs up, 2 is smile ect ect (for each user ew can also store their specific reaction in a anohter table to display their image but not implemeting that right now)
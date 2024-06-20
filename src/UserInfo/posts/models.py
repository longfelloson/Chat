from sqlalchemy import Column, Text, Integer, ForeignKey

from src.database import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    text = Column(Text)
    img_path = Column(Text, nullable=True)

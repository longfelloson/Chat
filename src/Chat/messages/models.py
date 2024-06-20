from datetime import datetime

from sqlalchemy import Integer, Column, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from src.database import Base


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False)
    text = Column(Text, nullable=False)
    sender = Column(Integer, nullable=False)
    receiver = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    chat = relationship("Chat", back_populates="messages")

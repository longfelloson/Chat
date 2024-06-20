from sqlalchemy import Integer, Column
from sqlalchemy.orm import relationship

from src.database import Base


class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    creator = Column(Integer, nullable=False)
    receiver = Column(Integer, nullable=False)

    messages = relationship("Message", back_populates="chat", lazy="selectin")

from typing import List, Optional

from sqlalchemy import insert, select, Column
from sqlalchemy.ext.asyncio import AsyncSession

from src.Chat.messages.models import Message


async def add_message(chat_id: int, text: str, sender: int, receiver: int, session: AsyncSession) -> int:
    """
    Adds a message to the database
    """
    await session.execute(insert(Message).values(chat_id=chat_id, text=text, sender=sender, receiver=receiver))
    await session.commit()


async def get_messages(
        chat_id: int,
        limit: int,
        session: AsyncSession,
        order_by: Column = None
) -> Optional[List[Message]]:
    """
    Gets all messages from the database
    """
    stmt = select(Message).where(Message.chat_id == chat_id)
    if order_by:
        stmt = stmt.order_by(order_by.desc())

    messages = await session.execute(stmt.limit(limit))
    return messages.scalars().all()

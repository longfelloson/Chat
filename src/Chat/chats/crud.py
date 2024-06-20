from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.Chat.chats.models import Chat


async def get_chat(chat_id: int, session: AsyncSession) -> Optional[Chat]:
    """
    Get a chat by its ID.
    """
    chat = await session.execute(select(Chat).where(Chat.id == chat_id))
    return chat.scalar_one_or_none()


async def get_chats(user_id: int, session: AsyncSession) -> Optional[List[Chat]]:
    """
    Get a chat by user's ID
    """
    chats = await session.execute(select(Chat).where(Chat.id == user_id))
    return chats.scalars().all()

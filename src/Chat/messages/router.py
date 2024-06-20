from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.Chat.messages import crud
from src.Chat.messages.models import Message
from src.UserInfo.auth.utils import auth_guard
from src.database import get_async_session

router = APIRouter(dependencies=[Depends(auth_guard)])


@router.get("/messages/get-messages")
async def get_messages_endpoint(
        chat_id: int,
        session: AsyncSession = Depends(get_async_session),
        limit: Optional[int] = 10
):
    """
    Get all messages from a chat
    """
    return await crud.get_messages(chat_id, limit, session, order_by=Message.created_at)

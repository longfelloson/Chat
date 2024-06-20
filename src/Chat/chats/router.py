from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates
from starlette.websockets import WebSocket, WebSocketDisconnect

from src.Chat.chats import crud
from src.Chat.chats.manager import chat_manager
from src.UserInfo.auth.utils import get_current_user, auth_guard
from src.UserInfo.users.models import User
from src.database import get_async_session

router = APIRouter(dependencies=[Depends(auth_guard)])
templates = Jinja2Templates(directory="../templates")


@router.get('/chats')
async def chats_page_endpoint(
        request: Request,
        user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    """
    Return page with all user's chats
    """
    chats = await crud.get_chats(user.id, session)
    return templates.TemplateResponse('/chats/chats.html', {'request': request, "chats": chats})


@router.get('/chat/{chat_id}')
async def chat_page_endpoint(request: Request, chat_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Returns chat page
    """
    chat = await crud.get_chat(chat_id, session)
    if not chat:
        return JSONResponse({'error': 'Chat not found'}, status_code=404)
    return templates.TemplateResponse("/chats/chat.html", {"request": request, "chat": chat})


@router.websocket("/chat/{chat_id}/{client_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        chat_id: int,
        client_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Chat WebSocket endpoint.
    """
    await chat_manager.connect(websocket, chat_id, client_id, session)
    try:
        while True:
            data = await websocket.receive_text()
            await chat_manager.broadcast(data, client_id, session)
    except WebSocketDisconnect:
        chat_manager.disconnect(websocket, client_id)

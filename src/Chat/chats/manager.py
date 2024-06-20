from fastapi import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from src.Chat.chats import crud
from src.Chat.chats.models import Chat
from src.Chat.messages import crud as messages_crud


class ChatManager:
    def __init__(self):
        self.chats = {}

    async def connect(self, websocket: WebSocket, chat_id: int, client_id: int, session: AsyncSession):
        """
        Connects to a websocket and create active connection
        """
        await websocket.accept()

        self.chats[client_id] = {
            "websocket": websocket, "chat": await crud.get_chat(chat_id, session),
            "connections": [websocket], "client_id": client_id
        }

    def disconnect(self, websocket: WebSocket, client_id: int):
        """
        Disconnects the websocket from the active connections
        """
        self.chats[client_id]['connections'].remove(websocket)

    async def broadcast(self, message: str, client_id: int, session: AsyncSession, add_to_database: bool = True):
        """
        Show messages for all members of chat
        """
        chat: Chat = self.chats[client_id]['chat']
        if add_to_database:
            await messages_crud.add_message(chat.id, message, chat.creator, chat.receiver, session)

        for connection in self.chats[client_id]['connections']:
            await connection.send_text(message)


chat_manager = ChatManager()

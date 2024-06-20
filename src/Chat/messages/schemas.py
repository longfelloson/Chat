from datetime import datetime

from pydantic import BaseModel


class NewMessage(BaseModel):
    chat_id: int
    sender: int
    recipient: int
    created_at: datetime

from pydantic import BaseModel
from datetime import datetime

class NotificationCreate(BaseModel):
    message: str

class Notification(BaseModel):
    id: int
    message: str
    is_sent: bool
    created_at: datetime

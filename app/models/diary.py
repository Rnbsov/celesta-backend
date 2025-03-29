from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DiaryEntryCreate(BaseModel):
    height: Optional[float] = None
    notes: Optional[str] = None
    image_url: Optional[str] = None

class DiaryEntry(BaseModel):
    id: int
    height: Optional[float] = None
    notes: Optional[str] = None
    image_url: Optional[str] = None
    date: datetime

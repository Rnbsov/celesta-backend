from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WateringCreate(BaseModel):
    watered_at: Optional[datetime] = None

class Watering(BaseModel):
    id: int
    watered_at: datetime

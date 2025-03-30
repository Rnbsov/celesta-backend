from pydantic import BaseModel
from typing import Optional
from datetime import date

class PlantCreate(BaseModel):
    name: str
    sowing_date: date
    substrate: Optional[str] = None
    expected_harvest_date: date
    plant_type: str

class Plant(BaseModel):
    id: int
    name: str
    sowing_date: date
    substrate: Optional[str] = None
    expected_harvest_date: date
    plant_type: str

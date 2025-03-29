from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ...models.plant import PlantCreate, Plant
from ...db import supabase
from ...dependencies import get_current_user

router = APIRouter(prefix="/plants", tags=["plants"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_plant(plant: PlantCreate, user_id: str = Depends(get_current_user)):
    try:
        # Insert plant using Supabase
        result = supabase.table('plants').insert({
            'name': plant.name,
            'sowing_date': plant.sowing_date.isoformat(),
            'substrate': plant.substrate,
            'expected_harvest_date': plant.expected_harvest_date.isoformat(),
            'user_id': user_id
        }).execute()
        
        return {"message": "Плантация добавлена"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[Plant])
async def get_plants(user_id: str = Depends(get_current_user)):
    try:
        # Get plants using Supabase
        response = supabase.table('plants').select(
            'id, name, sowing_date, substrate, expected_harvest_date'
        ).eq('user_id', user_id).execute()
        
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

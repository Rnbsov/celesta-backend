from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ...models.watering import WateringCreate, Watering
from ...db import supabase
from ...dependencies import get_current_user

router = APIRouter(tags=["watering"])

@router.post("/plants/{plant_id}/water", status_code=status.HTTP_201_CREATED)
async def water_plant(plant_id: int, watering: WateringCreate = None, user_id: str = Depends(get_current_user)):
    # Verify plant ownership
    plant_response = supabase.table('plants').select('id').eq('id', plant_id).eq('user_id', user_id).execute()
    
    if not plant_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Растение не найдено или у вас нет прав доступа"
        )
    
    try:
        data = {'plant_id': plant_id}
        if watering and watering.watered_at:
            data['watered_at'] = watering.watered_at.isoformat()
        
        supabase.table('watering_history').insert(data).execute()
        return {"message": "Полив зарегистрирован"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/plants/{plant_id}/watering", response_model=List[Watering])
async def get_watering_history(plant_id: int, user_id: str = Depends(get_current_user)):
    # Verify plant ownership
    plant_response = supabase.table('plants').select('id').eq('id', plant_id).eq('user_id', user_id).execute()
    
    if not plant_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Растение не найдено или у вас нет прав доступа"
        )
    
    try:
        watering_response = supabase.table('watering_history').select(
            'id, watered_at'
        ).eq('plant_id', plant_id).order('watered_at', desc=True).execute()
        
        return watering_response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

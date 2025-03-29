from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ...models.diary import DiaryEntryCreate, DiaryEntry
from ...db import supabase
from ...dependencies import get_current_user

router = APIRouter(prefix="/plants", tags=["diary"])

@router.post("/{plant_id}/diary", status_code=status.HTTP_201_CREATED)
async def add_diary_entry(plant_id: int, entry: DiaryEntryCreate, user_id: str = Depends(get_current_user)):
    # Verify plant ownership
    plant_response = supabase.table('plants').select('id').eq('id', plant_id).eq('user_id', user_id).execute()
    
    if not plant_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Растение не найдено или у вас нет прав доступа"
        )
    
    try:
        result = supabase.table('diary_entries').insert({
            'plant_id': plant_id,
            'height': entry.height,
            'notes': entry.notes,
            'image_url': entry.image_url
        }).execute()
        
        diary_id = result.data[0]['id']
        return {"message": "Запись добавлена", "id": diary_id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{plant_id}/diary", response_model=List[DiaryEntry])
async def get_diary_entries(plant_id: int, user_id: str = Depends(get_current_user)):
    # Verify plant ownership
    plant_response = supabase.table('plants').select('id').eq('id', plant_id).eq('user_id', user_id).execute()
    
    if not plant_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Растение не найдено или у вас нет прав доступа"
        )
    
    try:
        entries_response = supabase.table('diary_entries').select(
            'id, height, notes, image_url, date'
        ).eq('plant_id', plant_id).order('date', desc=True).execute()
        
        return entries_response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/diary/{entry_id}", status_code=status.HTTP_200_OK)
async def delete_diary_entry(entry_id: int, user_id: str = Depends(get_current_user)):
    # Check if entry belongs to user's plant
    entry_response = supabase.rpc('check_diary_entry_ownership', {'entry_id_param': entry_id, 'user_id_param': user_id}).execute()
    
    if not entry_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запись не найдена или у вас нет прав доступа"
        )
    
    try:
        supabase.table('diary_entries').delete().eq('id', entry_id).execute()
        return {"message": "Запись удалена"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

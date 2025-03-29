from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import List
from ...models.notification import NotificationCreate, Notification
from ...db import supabase
from ...dependencies import get_current_user

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_notification(notification: NotificationCreate, user_id: str = Depends(get_current_user)):
    try:
        result = supabase.table('notifications').insert({
            'user_id': user_id,
            'message': notification.message
        }).execute()
        
        notification_id = result.data[0]['id']
        return {"message": "Уведомление создано", "id": notification_id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[Notification])
async def get_notifications(user_id: str = Depends(get_current_user)):
    try:
        notifications_response = supabase.table('notifications').select(
            'id, message, is_sent, created_at'
        ).eq('user_id', user_id).order('created_at', desc=True).execute()
        
        return notifications_response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{notification_id}/mark-sent", status_code=status.HTTP_200_OK)
async def mark_notification_sent(notification_id: int, user_id: str = Depends(get_current_user)):
    # Verify notification ownership
    notification_response = supabase.table('notifications').select('id').eq('id', notification_id).eq('user_id', user_id).execute()
    
    if not notification_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Уведомление не найдено или у вас нет прав доступа"
        )
    
    try:
        supabase.table('notifications').update({'is_sent': True}).eq('id', notification_id).execute()
        return {"message": "Уведомление отмечено как отправленное"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

def generate_notifications_task():
    """Background task to generate notifications"""
    try:
        # Get plants with upcoming harvest dates
        harvest_response = supabase.rpc('get_plants_for_harvest_notifications').execute()
        harvest_reminders = harvest_response.data
        
        for plant in harvest_reminders:
            supabase.table('notifications').insert({
                'user_id': plant['user_id'],
                'message': f"Приближается дата сбора урожая для {plant['name']} ({plant['expected_harvest_date']})"
            }).execute()
        
        # Get plants needing watering
        watering_response = supabase.rpc('get_plants_for_watering_notifications').execute()
        watering_reminders = watering_response.data
        
        for plant in watering_reminders:
            supabase.table('notifications').insert({
                'user_id': plant['user_id'],
                'message': f"Не забудьте полить {plant['name']}! Последний полив был более 3 дней назад."
            }).execute()
            
    except Exception as e:
        print(f"Ошибка при генерации уведомлений: {str(e)}")

@router.post("/admin/generate-notifications", status_code=status.HTTP_200_OK)
async def manual_generate_notifications(background_tasks: BackgroundTasks, user_id: str = Depends(get_current_user)):
    background_tasks.add_task(generate_notifications_task)
    return {"message": "Уведомления будут сгенерированы в фоновом режиме"}

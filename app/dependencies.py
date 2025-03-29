from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .db import supabase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        auth = supabase.auth.get_user(token)
        user_id = auth.user.id
        # Authenticate for DB requests
        supabase.postgrest.auth(token)  
        return user_id
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

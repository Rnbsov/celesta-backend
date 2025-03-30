from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .db import supabase

# Replace OAuth2PasswordBearer with HTTPBearer for simple token auth
security = HTTPBearer(
    scheme_name="Bearer Authentication",
    description="Enter your Bearer token",
    auto_error=True
)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        token = credentials.credentials
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

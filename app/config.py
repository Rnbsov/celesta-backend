import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY")
    
    # Swagger settings
    SWAGGER_URL: str = "/docs"  # FastAPI automatically serves Swagger UI at /docs
    
    class Config:
        env_file = ".env"

settings = Settings()

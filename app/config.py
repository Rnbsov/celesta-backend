import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY")
    
    # Redis settings
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    REDIS_URL: str = os.getenv("REDIS_URL", f"redis://{REDIS_HOST}:{REDIS_PORT}")
    
    # Cache settings
    CACHE_EXPIRATION_IN_SECONDS: int = int(os.getenv("CACHE_EXPIRATION_IN_SECONDS", "360"))
    
    # Swagger settings
    SWAGGER_URL: str = "/docs"  # FastAPI automatically serves Swagger UI at /docs
    
    class Config:
        env_file = ".env"

settings = Settings()

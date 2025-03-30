import json
import pickle
from functools import wraps
from typing import Any, Callable, Optional
from fastapi import Request, Response
import redis.asyncio as redis_asyncio

from .config import settings

# Global Redis client
redis_client = None

async def setup_redis_cache():
    """Initialize Redis cache connection"""
    global redis_client
    redis_client = redis_asyncio.from_url(
        settings.REDIS_URL,
        password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
        decode_responses=False  # Need binary for pickle serialization
    )
    # Test connection
    await redis_client.ping()
    return redis_client

def get_cache_key(namespace: str, func_name: str, user_id: str, args_str: str) -> str:
    """Generate a cache key for the given function and arguments"""
    return f"celesta-cache:{namespace}:{func_name}:{user_id}:{args_str}"

def cached(namespace: str = "", expire_seconds: int = None):
    """
    Custom cache decorator for FastAPI route handlers
    
    Args:
        namespace: Namespace to use for cache keys
        expire_seconds: Cache TTL in seconds, defaults to config setting if None
    """
    expiration = expire_seconds or settings.CACHE_EXPIRATION_IN_SECONDS
    
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            global redis_client
            if redis_client is None:
                # If Redis isn't connected yet, just execute the function
                return await func(*args, **kwargs)
                
            # Extract request from args or kwargs
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            if not request and 'request' in kwargs:
                request = kwargs['request']
                
            # Get user_id from request state or use 'anonymous'
            user_id = "anonymous"
            if request and hasattr(request, "state") and hasattr(request.state, "user_id"):
                user_id = request.state.user_id
                
            # Create a cache key from function name and arguments
            func_name = f"{func.__module__}.{func.__name__}"
            kwargs_str = json.dumps({k: str(v) for k, v in kwargs.items() if k != 'request'}, sort_keys=True)
            cache_key = get_cache_key(namespace, func_name, user_id, kwargs_str)
            
            # Try to get data from cache
            cached_data = await redis_client.get(cache_key)
            if cached_data:
                return pickle.loads(cached_data)
                
            # If not in cache, execute the function
            result = await func(*args, **kwargs)
            
            # Store result in cache
            await redis_client.set(
                cache_key,
                pickle.dumps(result),
                ex=expiration
            )
            
            return result
        return wrapper
    return decorator

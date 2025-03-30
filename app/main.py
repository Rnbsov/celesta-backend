from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference
from app.api.routes import auth, plants, diary, watering, notifications

app = FastAPI(title="Celesta backend", description="An amazing Celesta backend API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(auth.router)
app.include_router(plants.router)
app.include_router(diary.router)
app.include_router(watering.router)
app.include_router(notifications.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Celesta backend API"}

# Scalar API documentation
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title
    )

# Setup middleware to store user_id in request state for cache key generation
@app.middleware("http")
async def add_user_to_request_state(request: Request, call_next):
    # Get authorization header
    auth_header = request.headers.get("Authorization", "")
    if auth_header and auth_header.startswith("Bearer "):
        try:
            token = auth_header.replace("Bearer ", "")
            # We have to duplicate some auth logic here
            # to avoid circular imports with dependencies
            from app.db import supabase
            auth = supabase.auth.get_user(token)
            print(auth)
            request.state.user_id = auth.user.id
        except Exception:
            pass
    
    response = await call_next(request)
    return response

@app.on_event("startup")
async def startup_event():
    # Initialize Redis cache on startup
    await setup_redis_cache()

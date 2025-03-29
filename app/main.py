from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

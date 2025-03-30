from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from scalar_fastapi import get_scalar_api_reference
from app.api.routes import auth, plants, diary, watering, notifications
from app.cache import setup_redis_cache
from app.dependencies import get_current_user

# Create FastAPI app with customized security settings
app = FastAPI(
    title="Celesta backend", 
    description="An amazing Celesta backend API",
    # Disable the default documentation
    docs_url=None, 
)

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

# Custom OpenAPI schema with Bearer token security
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description=app.description,
        routes=app.routes,
    )
    
    # Make sure components is in the schema
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    
    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your Bearer token in the format **Bearer &lt;token&gt;**"
        }
    }
    
    # Add global security requirement
    openapi_schema["security"] = [{"BearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Replace the OpenAPI schema with our custom schema
app.openapi = custom_openapi

# Custom Swagger UI route
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )

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

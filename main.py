import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from config import get_settings
from database import Base, engine
from routers import posts_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize settings
settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url="/api/redoc",
)

# Add middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],  # Update this for production
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(posts_router)


# Health check endpoint
@app.get("/api/health", tags=["health"])
def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.API_VERSION}


@app.get("/", tags=["root"])
def root() -> dict:
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.API_TITLE} API",
        "version": settings.API_VERSION,
        "docs_url": "/api/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )

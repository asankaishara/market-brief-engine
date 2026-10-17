from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.endpoints import ingest

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0"
)

# Include API routers
app.include_router(ingest.router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "project": settings.PROJECT_NAME
    }
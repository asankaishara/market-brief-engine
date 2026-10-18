from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.endpoints import ingest, search
import logging
import logging.config
import os

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0"
)

# Include API routers
app.include_router(ingest.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "project": settings.PROJECT_NAME
    }

# 1. Find the path to your logging.ini file
config_path = os.path.join(os.path.dirname(__file__), "logging.ini")

# 2. Load the configuration universally
logging.config.fileConfig(config_path)

# 3. Create a logger for this file and use it
logger = logging.getLogger(__name__)

logger.info("Application has started successfully using the universal config!")
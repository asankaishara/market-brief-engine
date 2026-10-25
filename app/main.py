import logging
import logging.config
import os

# Configure logging BEFORE importing any app modules
config_path = os.path.join(os.path.dirname(__file__), "logging.ini")
logging.config.fileConfig(config_path, disable_existing_loggers=False)

from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.endpoints import ingest, search
from app.api.v1.endpoints import brief

# create logger
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0"
)

# Include API routers
app.include_router(ingest.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")
app.include_router(brief.router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "project": settings.PROJECT_NAME
    }

logger.info("Application has started successfully using the universal config!")
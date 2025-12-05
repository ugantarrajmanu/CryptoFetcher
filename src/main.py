from fastapi import FastAPI
from src.config import settings

app = FastAPI(
    title = settings.APP_NAME,
    version = settings.APP_VERSION,
    description = "API for CryptoFetcher"
    
)

@app.get("/health")
async def health_check():
    try:
        await client._get("/ping")
        status = "healthy"
        upstream = "connected"
    except Exception:
        status = "degraded"
        upstream = "disconnected"

    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": status,
        "upstream_service": upstream
    }
from fastapi import FastAPI, Depends, Query, HTTPException
from src.config import settings
from src.auth import verify_token


app = FastAPI(
    title = settings.APP_NAME,
    version = settings.APP_VERSION,
    description = "API for CryptoFetcher"
    
)

@app.get("/health", tags=["Health"])
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


# list all coins
@app.get("/api/v1/coins", dependencies=[Depends(verify_token)], tags=["Coins"])
async def list_all_coins(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=250, description="Items per page")
):

    try:
        all_coins = await client.get_coin_list()
        
        start = (page - 1) * per_page
        end = start + per_page
        
        paginated_items = all_coins[start:end]
        
        return {
            "page": page,
            "per_page": per_page,
            "total_items": len(all_coins),
            "data": paginated_items
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


# list all coin categories
@app.get("/api/v1/categories", dependencies=[Depends(verify_token)], tags=["Coins"])
async def list_categories():
    try:
        categories = await client.get_categories()
        return {"data": categories}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))



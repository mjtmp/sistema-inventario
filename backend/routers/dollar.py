from fastapi import APIRouter, Depends
from services.dollar_service import get_dollar_rate
from cachetools import TTLCache

router = APIRouter()

# Cache para almacenar el resultado del scraping
cache = TTLCache(maxsize=1, ttl=3600)

@router.get("/dollar-rate", response_model=dict)
async def get_dollar():
    cache_result = cache.get("scraped_data")
    
    if cache_result:
        return cache_result
    else:
        result = await get_dollar_rate()
        cache["scraped_data"] = result
        return result

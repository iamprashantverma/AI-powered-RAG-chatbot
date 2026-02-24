from fastapi import APIRouter
from app.services.health_service import get_health_status

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("")
async def health():
    return await get_health_status()

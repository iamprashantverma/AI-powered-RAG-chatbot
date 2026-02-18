from fastapi import APIRouter,Depends
from app.api.chat_routes import router as chat_router
from app.api.health_routes import router as health_router
from app.api.auth_routes import router as auth_router
from app.api.deps import get_current_user

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(chat_router,dependencies=[Depends(get_current_user)])

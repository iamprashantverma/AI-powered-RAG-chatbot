from fastapi import APIRouter,Depends
from app.api.v1.chat_routes import router as chat_router
from app.api.v1.health_routes import router as health_router
from app.api.v1.auth_routes import router as auth_router
from app.api.deps import get_current_user
from app.api.v1.docs_route import router as docs_router
api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(docs_router,dependencies=[Depends(get_current_user)])
api_router.include_router(chat_router,dependencies=[Depends(get_current_user)])

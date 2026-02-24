from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, LoginResponse
from app.services.auth_service import login_service
from app.api.deps import get_db 
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user_service

router = APIRouter(prefix="/auth")

@router.post("/login", response_model=LoginResponse)
def login_(login_cred: LoginRequest, db: Session = Depends(get_db)):
    return login_service(db, login_cred)


@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(db, user)
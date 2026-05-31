from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.deps import get_db
from app.schemas.auth import LoginRequest, LoginResponse
from app.schemas.user import UserCreate, UserResponse
from app.services import auth as auth_service
from app.services.user import create_user

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login_user(body.email, body.password, db)


@router.post("/login/form", response_model=LoginResponse)
def login_form(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return auth_service.login_user(form.username, form.password, db)



@router.post("/register", response_model=UserResponse)
def register(body: UserCreate, db: Session = Depends(get_db)):
    return create_user(body, db)
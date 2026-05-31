



from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import LoginResponse
from app.services.user import get_user_by_email
from app.core.security import create_access_token, create_refresh_token, verify_password


def login_user(email: str, pwd: str, db: Session) -> LoginResponse:
    user = get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user or not user.is_active or user.deleted_at:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your account has been deactivated, please contact support")    
    if not verify_password(pwd, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    return LoginResponse(access_token=access_token, refresh_token=refresh_token, user=user)
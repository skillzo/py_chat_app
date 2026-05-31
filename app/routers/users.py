from fastapi import APIRouter, status

from app.schemas.user import UserCreate, UserResponse



router = APIRouter()




router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db):
    return db.create_user(user)
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services import user as user_service

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Return the currently authenticated user."""
    return current_user

@router.get("", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    """Return all users."""
    return user_service.get_all_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    """Return a specific user by their ID."""
    user = user_service.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user_endpoint(
    user_id: UUID,
    user: UserCreate,
    db: Session = Depends(get_db),
):
    update = UserUpdate(id=user_id, **user.model_dump())
    return user_service.update_user(update, db)


@router.delete("/{user_id}")
def delete_user_endpoint(user_id: UUID, db: Session = Depends(get_db)):
    return {"detail": user_service.delete_user(user_id, db)}

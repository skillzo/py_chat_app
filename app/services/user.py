import datetime
from uuid import UUID
from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.models.user import User
from app.core.logging import get_logger
from app.schemas.user import UserCreate, UserUpdate

logger = get_logger(__name__)

def get_user_by_email(email: str, db: Session)-> User | None:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    return user


def get_user_by_username(username: str, db: Session)-> User | None:
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(id: UUID, db: Session)-> User | None:
    return db.query(User).filter(User.id == id).first()



def create_user(user: UserCreate, db: Session) -> User:
    if get_user_by_email(user.email.lower(), db) or get_user_by_username(
        user.username.strip(), db
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email address or username already exists",
        )
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username.strip(), email=user.email.lower(), password=hashed_password)
    db.add(new_user)
    try: 
        db.commit()
    except Exception as e:    
        db.rollback()
        logger.exception("failed_to_create_user", email=user.email)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to create user")
    db.refresh(new_user)
    return new_user



def update_user(user: UserUpdate , db: Session) -> User:
    user_exists = get_user_by_id(user.id, db)
    if not user_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_exists.username = user.username.strip()
    user_exists.email = user.email.lower()
    db.commit()
    db.refresh(user_exists)
    return user_exists



def delete_user(id: UUID, db: Session) -> str:
    user_exists = get_user_by_id(id, db)
    if not user_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_exists.is_active = False
    user_exists.deleted_at = datetime.datetime.now(datetime.timezone.utc)
    db.commit()
    return "User deleted successfully"



def get_all_users(db: Session) -> list[User]:
    return db.query(User).filter(User.is_active == True, User.deleted_at == None).order_by(User.created_at.desc()).all()


   
def change_password(id: UUID, pwd: str, db: Session) -> str:
    user_exists = get_user_by_id(id, db)
    if not user_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_exists.password = hash_password(pwd)
    db.commit()
    return "Password changed successfully"
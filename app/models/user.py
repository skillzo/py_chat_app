



from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
import uuid
from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column((UUID), primary_key=True, default=uuid.uuid4)    
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
                        DateTime(timezone=True), 
                        default=lambda: datetime.now(timezone.utc), 
                        nullable=False
                        )
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"
    
    
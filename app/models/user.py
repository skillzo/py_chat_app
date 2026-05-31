



from datetime import datetime
from time import timezone
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
import uuid
from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)    
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
                        DateTime(timezone=True), 
                        default=lambda: datetime.now(timezone.utc), 
                        nullable=False
                        )
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"
    
    
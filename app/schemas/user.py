from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str



class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID    
    username: str
    email: str
    created_at: datetime
    updated_at: datetime
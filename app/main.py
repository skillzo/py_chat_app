from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logging import RequestLoggingMiddleware, setup_logging
from app.database import Base, engine
from app.models import user as user_model  # noqa: F401
from app.routers import auth, users

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan, title="Py Chat", description="A simple chat application", version="0.1.0")
app.add_middleware(RequestLoggingMiddleware)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

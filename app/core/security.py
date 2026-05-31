import datetime
import uuid

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from jose import JWTError, jwt

from app.core.config import settings

password_hasher = PasswordHasher()


def hash_password(pwd: str) -> str:
    return password_hasher.hash(pwd)


def verify_password(plain_pwd: str, hashed_pwd: str) -> bool:
    try:
        password_hasher.verify(hashed_pwd, plain_pwd)
        return True
    except (VerifyMismatchError, InvalidHashError):
        return False


def create_access_token(data: dict) -> str:
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )
    payload = {
        "sub": str(data["sub"]),
        "exp": expire,
        "type": "access",
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "jti": str(uuid.uuid4()),
        "iss": "py_chat",
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_refresh_token(data: dict) -> str:
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        minutes=settings.jwt_refresh_token_expire_minutes
    )
    payload = {
        "sub": str(data["sub"]),
        "exp": expire,
        "type": "refresh",
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "jti": str(uuid.uuid4()),
        "iss": "py_chat",
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError:
        return None

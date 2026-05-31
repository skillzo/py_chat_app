


from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecate='false')



def hash_password(pwd: str):
    return pwd_context.hash(pwd)


def verify_password(plain_pwd: str, hashed_pwd: str):
    return pwd_context.verify(plain_pwd, hashed_pwd)


def get_password_hash(password: str):
    return pwd_context.hash(password)


# =========================
# auth/users.py - FastAPI Users setup
# =========================
import uuid
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTStrategy, AuthenticationBackend
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.manager import BaseUserManager
from db import AsyncSessionLocal
from models import User
from fastapi import Depends


async def get_user_db():  # type: ignore
    async with AsyncSessionLocal() as session:
        yield SQLAlchemyUserDatabase(session, User)


class UserManager(BaseUserManager[User, uuid.UUID]):
    async def on_after_register(self, user: User, request=None):  # type: ignore
        print(f"User {user.id} has registered.")


async def get_user_manager(user_db=Depends(get_user_db)):  # type: ignore
    yield UserManager(user_db)

# JWT Authentication backend
# Type warnings are expected with FastAPI Users async setup
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

jwt_strategy = JWTStrategy(
    secret=os.getenv("SECRET_KEY", "dev_secret_key_change_in_production"),
    lifetime_seconds=3600,
)  # type: ignore

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=jwt_strategy,
    get_strategy=lambda: jwt_strategy,
)  # type: ignore

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)  # type: ignore 
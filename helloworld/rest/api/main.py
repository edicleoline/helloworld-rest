from fastapi import APIRouter

from .routes import authentication
from .routes import account

api_router = APIRouter()
api_router.include_router(authentication.router, tags=["authentication"])
api_router.include_router(account.router, tags=["account"])
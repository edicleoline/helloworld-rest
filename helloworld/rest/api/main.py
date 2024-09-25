from fastapi import APIRouter

from .routes import authenticate
from .routes import account

api_router = APIRouter()
api_router.include_router(authenticate.router, tags=["authentication"])
api_router.include_router(account.router, tags=["account"])
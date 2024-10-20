from fastapi import APIRouter

from .routes import authentication
from .routes import account
from .routes import phone
from .routes import client

api_router = APIRouter()
api_router.include_router(authentication.router, tags=["authentication"])
api_router.include_router(account.router, tags=["account"])
api_router.include_router(phone.router, tags=["phone"])
api_router.include_router(client.router, tags=["client"])
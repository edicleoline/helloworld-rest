from fastapi import APIRouter

from .routes import authentication
from .routes import account
from .routes import device
from .routes import phone

api_router = APIRouter()
api_router.include_router(authentication.router, tags=["authentication"])
api_router.include_router(account.router, tags=["account"])
api_router.include_router(device.router, tags=["device"])
api_router.include_router(phone.router, tags=["phone"])
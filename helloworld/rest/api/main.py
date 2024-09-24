from fastapi import APIRouter

from .routes import authenticate

api_router = APIRouter()
api_router.include_router(authenticate.router, tags=["authentication"])
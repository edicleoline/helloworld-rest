from __future__ import annotations

from fastapi.security import OAuth2PasswordBearer
from helloworld.rest.config import settings

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/identify"
)
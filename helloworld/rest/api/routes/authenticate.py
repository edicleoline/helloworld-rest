from __future__ import annotations

from fastapi import APIRouter

from helloworld.auth.features.authentication import get_identify_use_case, get_authenticate_use_case
from helloworld.auth.features.authentication.entities import ResponseEntity
from helloworld.account.features.user import UserEntity

router = APIRouter()

@router.post("/auth/identify")
async def identity(identifier: str) -> str | None:
    identify_use_case = await get_identify_use_case()
    token = await identify_use_case.execute(identifier=identifier)

    return token

@router.post("/auth/access-token")
async def authenticate(token: str, password: str | None = None, user: UserEntity | None = None) -> ResponseEntity | None:
    authenticate_use_case = await get_authenticate_use_case()
    response = await authenticate_use_case.execute(token=token, password=password, user=user)

    return response


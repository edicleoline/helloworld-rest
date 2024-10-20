from __future__ import annotations

from fastapi import APIRouter, Depends

from helloworld.account.features.user import get_me_use_case, UserEntity
from helloworld.rest.api import oauth2_scheme

router = APIRouter()

@router.get("/me")
async def me(token: str = Depends(oauth2_scheme)) -> UserEntity | None:
    me_use_case = await get_me_use_case(token)
    user = await me_use_case.execute()

    return user





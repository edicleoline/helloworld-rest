from __future__ import annotations

from fastapi import APIRouter

from helloworld.auth.features.authentication import get_identify_use_case, get_authenticate_use_case

router = APIRouter()

@router.post("/auth/identify")
async def auth_identity(identifier: str) -> str | None:
    identify_use_case = await get_identify_use_case()
    token = await identify_use_case.execute(identifier=identifier)

    return token


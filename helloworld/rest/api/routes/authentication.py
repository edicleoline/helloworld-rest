from __future__ import annotations

from pydantic import BaseModel
from fastapi import APIRouter

from helloworld.auth.features.authentication import get_identify_use_case, get_authenticate_use_case, AuthenticateResponseEntity, IdentifyResponseEntity
from helloworld.account.features.user import UserEntity

router = APIRouter()

class IdentityRequest(BaseModel):
    identifier: str

class AuthenticateRequest(BaseModel):
    token: str
    password: str | None
    user: UserEntity | None


@router.post("/auth/identify")
async def identity(body: IdentityRequest) -> IdentifyResponseEntity | None:
    identify_use_case = await get_identify_use_case()
    response = await identify_use_case.execute(identifier=body.identifier)

    return response

@router.post("/auth/access-token")
async def authenticate(body: AuthenticateRequest) -> AuthenticateResponseEntity | None:
    authenticate_use_case = await get_authenticate_use_case()
    response = await authenticate_use_case.execute(token=body.token, password=body.password, user=body.user)

    return response


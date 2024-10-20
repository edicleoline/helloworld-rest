from __future__ import annotations

from collections.abc import Sequence

from pydantic import BaseModel
from fastapi import APIRouter

from helloworld.core.util.json import jsonify
from helloworld.account.features.phone import PhoneEntity, get_find_or_create_use_case
from helloworld.account.features.phone_verifier import (
    get_start_use_case, PhoneVerifierStartEntity, get_verify_use_case, get_methods_use_case, MethodEntity)

router = APIRouter()

class PhoneRequest(BaseModel):
    phone_number: str

class VerifyRequest(BaseModel):
    token: str
    otp_code: str

class StartRequest(BaseModel):
    phone_id: int
    device_id: int
    method: str


@router.post("/phone")
async def phone(body: PhoneRequest) -> PhoneEntity | None:
    find_or_create_use_case = await get_find_or_create_use_case()
    entity = await find_or_create_use_case.execute(phone_number=body.phone_number)
    return entity

@router.post("/phone/verifier/start")
async def start(body: StartRequest) -> PhoneVerifierStartEntity | None:
    start_use_case = await get_start_use_case()
    entity = await start_use_case.execute(phone_id=body.phone_id, device_id=body.device_id, method=body.method)
    return entity

@router.post("/phone/verifier/verify")
async def verify(body: VerifyRequest) -> None:
    verify_use_case = await get_verify_use_case()
    await verify_use_case.execute(token=body.token, otp_code=body.otp_code)

@router.get("/phone/verifier/method/device/{device_id}")
async def methods_by_device(device_id: int) -> Sequence[MethodEntity]:
    methods_use_case = await get_methods_use_case()
    return await methods_use_case.execute(device_id=device_id)



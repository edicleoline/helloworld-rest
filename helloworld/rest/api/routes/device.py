from __future__ import annotations

from collections.abc import Sequence
from pydantic import BaseModel

from helloworld.auth.features.identity import IdentityEntity
from helloworld.account.features.device import get_install_use_case, DeviceEntity
from helloworld.auth.features.device_otp import OTPType
from helloworld.account.features.device_verifier import (
    get_start_use_case, DeviceVerifierStartEntity, get_verify_use_case, get_methods_use_case, MethodEntity,
    StartUseCaseRequest)

from fastapi import APIRouter


router = APIRouter()

class VerifyRequest(BaseModel):
    token: str
    otp_code: str

class StartRequest(BaseModel):
    target_id: int
    device_id: int
    method: str

@router.post("/device/install")
async def register_device(device: DeviceEntity) -> DeviceEntity | None:
    install_use_case = await get_install_use_case()
    return await install_use_case.execute(device=device)

@router.post("/device/verifier/start")
async def start(body: StartRequest) -> DeviceVerifierStartEntity | None:
    start_use_case = await get_start_use_case()
    return await start_use_case.execute(StartUseCaseRequest(
        target_id=body.target_id,
        device_id=body.device_id,
        otp_type=OTPType.from_string(body.method)
    ))

@router.post("/device/verifier/verify")
async def verify(body: VerifyRequest) -> IdentityEntity | None:
    verify_use_case = await get_verify_use_case()
    return await verify_use_case.execute(token=body.token, otp_code=body.otp_code)

@router.get("/device/{device_id}/verifier/target/{target_id}/method")
async def methods_by_device(target_id: int, device_id: int) -> Sequence[MethodEntity]:
    methods_use_case = await get_methods_use_case()
    return await methods_use_case.execute(target_id=target_id, device_id=device_id)



from __future__ import annotations

from fastapi import APIRouter

from helloworld.account.features.device import get_install_use_case, DeviceEntity

router = APIRouter()

@router.post("/client/install")
async def register_device(device: DeviceEntity) -> DeviceEntity | None:
    install_use_case = await get_install_use_case()
    response = await install_use_case.execute(device=device)

    return response

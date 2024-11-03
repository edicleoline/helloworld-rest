from __future__ import annotations

from pydantic import BaseModel

from helloworld.account.features.phone import PhoneEntity, get_find_or_create_use_case

from fastapi import APIRouter


router = APIRouter()

class PhoneRequest(BaseModel):
    phone_number: str

@router.post("/phone")
async def phone(body: PhoneRequest) -> PhoneEntity | None:
    find_or_create_use_case = await get_find_or_create_use_case()
    entity = await find_or_create_use_case.execute(phone_number=body.phone_number)
    return entity
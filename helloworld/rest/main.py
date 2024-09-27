from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from helloworld.rest.helloworld import init
from helloworld.rest.api.main import api_router
from helloworld.rest.config import settings
from helloworld.auth.error import exceptions

app = FastAPI(
    title=settings.PROJECT_NAME
)

app.include_router(api_router, prefix=settings.API_V1_STR)

app.add_event_handler("startup", init)


@app.exception_handler(exceptions.InvalidLoginOrPasswordError)
async def invalid_login_exception_handler(request, exc: exceptions.InvalidLoginOrPasswordError):
    return JSONResponse(
        status_code=401,
        content={
            "detail": "Invalid login or password."
        },
    )
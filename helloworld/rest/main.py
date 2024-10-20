from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from helloworld.rest.helloworld import init
from helloworld.rest.api.main import api_router
from helloworld.rest.config import settings
from helloworld.auth.error import exceptions
from helloworld.core.error import exceptions as core_exceptions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME
)

app.include_router(api_router, prefix=settings.API_V1_STR)

app.add_event_handler("startup", init)


@app.middleware("http")
async def log_request(request: Request, call_next):
    body = await request.body()
    logger.info(f"Request body: {body.decode('utf-8')}")  # Decodifica o corpo para uma string
    response = await call_next(request)
    return response

@app.exception_handler(exceptions.InvalidLoginOrPasswordError)
async def invalid_login_exception_handler(request, exc: exceptions.InvalidLoginOrPasswordError):
    return JSONResponse(
        status_code=401,
        content={
            "detail": "Invalid login or password.",
            "code": 1020
        },
    )

@app.exception_handler(exceptions.InvalidTokenError)
async def invalid_token_exception_handler(request, exc: exceptions.InvalidTokenError):
    return JSONResponse(
        status_code=401,
        content={
            "detail": "Invalid token.",
            "code": 1023
        },
    )

@app.exception_handler(core_exceptions.InvalidOTPCodeError)
async def argument_exception_handler(request, exc: exceptions.InvalidLoginOrPasswordError):
    return JSONResponse(
        status_code=401,
        content={
            "detail": "The code entered is incorrect. Please try again.",
            "code": 1040
        },
    )

@app.exception_handler(core_exceptions.UnauthorizedError)
async def argument_exception_handler(request, exc: exceptions.InvalidLoginOrPasswordError):
    return JSONResponse(
        status_code=401,
        content={
            "detail": "You can not do this.",
            "code": 1045
        },
    )

@app.exception_handler(core_exceptions.OTPRequestLimitError)
async def argument_exception_handler(request, exc: exceptions.InvalidLoginOrPasswordError):
    return JSONResponse(
        status_code=401,
        content={
            "detail": "You can not do this now.",
            "code": 1046
        },
    )

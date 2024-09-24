from __future__ import annotations

from fastapi import FastAPI

from helloworld.rest.helloworld import init
from helloworld.rest.api.main import api_router
from helloworld.rest.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME
)

app.include_router(api_router, prefix=settings.API_V1_STR)

app.add_event_handler("startup", init)

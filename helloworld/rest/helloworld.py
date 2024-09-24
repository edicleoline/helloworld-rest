from __future__ import annotations

from typing import Sequence, Dict

from helloworld.core.services import service_manager
from helloworld.core.util import load_class_from_string
from helloworld.auth.jwt.services import JWTService
from .config import settings


def db_session_manager_after_commit(enitities: Sequence[Dict]):
    # print("after_commit", enitities)
    pass

async def init_databases():
    services = settings.database_services

    for service in services:
        service_name = service.pop('SERVICE_NAME', None)
        service_type_str = service.pop('SERVICE_TYPE', None)

        service_type = load_class_from_string(service_type_str)
        dynamic_kwargs = {key.lower(): value for key, value in service.items()}

        (await service_manager.register("database", service_name, service_type)) \
            .init(**dynamic_kwargs) \
            .listen("after_commit", db_session_manager_after_commit)


async def init_tokens():
    services = settings.token_services

    for service in services:
        service_name = service.pop('SERVICE_NAME', None)

        dynamic_kwargs = {key.lower(): value for key, value in service.items()}

        (await service_manager.register("authentication", service_name, JWTService)) \
            .init(**dynamic_kwargs)


async def init():
    print("Lets init Helloworld with config", settings)

    await init_databases()
    await init_tokens()
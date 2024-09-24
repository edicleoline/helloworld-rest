from __future__ import annotations

import os
from typing import List, Dict

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from helloworld.core.util import cast_value


from dotenv import load_dotenv
load_dotenv("../../.env")


def _load_dynamic_services(prefix: str) -> List[Dict] | None:
    services: Dict = {}

    for key, value in os.environ.items():
        if key.startswith(prefix):
            parts = key.split('_')
            service_name = parts[1]
            config_key = '_'.join(parts[2:])

            if service_name not in services:
                services[service_name] = {}

            services[service_name][config_key] = cast_value(value)

    return list(services.values())


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"

    PROJECT_NAME: str

    _database_services: List[Dict] = []
    _token_services: List[Dict] = []

    def __init__(self, **values):
        super().__init__(**values)
        self._database_services = _load_dynamic_services("DATABASE_")
        self._token_services = _load_dynamic_services("TOKEN_")

    @computed_field
    @property
    def database_services(self) -> List[Dict]:
        return self._database_services

    @computed_field
    @property
    def token_services(self) -> List[Dict]:
        return self._token_services


settings = Settings()
from __future__ import annotations

from typing import Sequence, Dict

from aiokafka.errors import KafkaConnectionError

from helloworld.core.services import service_manager
from helloworld.core.util import load_class_from_string
from helloworld.auth.jwt.services import JWTService
from helloworld.core.messaging import Template
from helloworld.core.phoning import SMSService, CallService
from helloworld.core.notification import NotificationService
from helloworld.core.mailing import MailingService
from helloworld.core.infra.queuing import KafkaProducer
from helloworld.core.infra.mailing import MailingKafkaSender
from helloworld.core.infra.phoning import SMSKafkaSender, CallKafkaSender, PhonenumbersService
from helloworld.core.infra.notification import NotificationKafkaSender
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


async def init_queuing():
    try:
        await ((await service_manager.register("queuing", "mailing", KafkaProducer))
            .init(bootstrap_servers="localhost:9092")) \
            .start()
    except KafkaConnectionError: pass

    try:
        await ((await service_manager.register("queuing", "sms", KafkaProducer))
            .init(bootstrap_servers="localhost:9093")) \
            .start()
    except KafkaConnectionError: pass

    try:
        await ((await service_manager.register("queuing", "call", KafkaProducer))
            .init(bootstrap_servers="localhost:9094")) \
            .start()
    except KafkaConnectionError: pass

    try:
        await ((await service_manager.register("queuing", "notification", KafkaProducer))
            .init(bootstrap_servers="localhost:9095")) \
            .start()
    except KafkaConnectionError: pass


async def init_mailing():
    main_mailing = await service_manager.register("mailing", "main", MailingService)
    main_mailing.templates.register(Template("welcome", "en", "<html>Welcome, {{ first_name }}!</html>"))
    main_mailing.templates.register(Template("welcome", "pt", "<html>Bem-vindo, {{ first_name }}!</html>"))
    main_mailing.senders.register(sender_class=MailingKafkaSender, priority="critical",
                                  producer=service_manager.get("queuing", "mailing"))
    # await main_mailing.send("welcome", "en", "joao@test.com", "subject test")


async def init_phoning():
    sms_service = await service_manager.register("phoning", "sms", SMSService)
    sms_service.templates.register(Template("otp", "en", "Your code is {{ code }}"))
    sms_service.senders.register(sender_class=SMSKafkaSender, priority="critical", producer=service_manager.get("queuing", "sms"))
    # await main_phoning.send("otp", "en", "11998765432", code=123456)

    dial_service = await service_manager.register("phoning", "call", CallService)
    dial_service.senders.register(sender_class=CallKafkaSender, priority="critical", producer=service_manager.get("queuing", "call"))
    # await dial_service.send("otp", "en", "11998765432", code=123456)

    phone_service = await service_manager.register("phoning", "main", PhonenumbersService)
    # a = phone_service.format_number("+5511994423173")


async def init_notification():
    main_notification = await service_manager.register("notification", "main", NotificationService)
    main_notification.templates.register(Template("otp", "en", "Requested otp app {{ code }}"))
    main_notification.senders.register(sender_class=NotificationKafkaSender, priority="critical",
                                       producer=service_manager.get("queuing", "notification"))
    # await main_notification.send(123, "en", "notification title", "otp", {}, "critical", code="123456")

async def init():
    print("Lets init Helloworld with config", settings)

    await init_databases()
    await init_tokens()
    await init_queuing()
    await init_mailing()
    await init_phoning()
    await init_notification()
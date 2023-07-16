import asyncio

import httpx
import pytest
from aerich import Command
from tortoise import Tortoise

from src.main import app
from src.settings import (
    DB_NAME_TEST,
    DB_USER_TEST,
    DB_PASS_TEST,
    DB_HOST_TEST,
    DB_PORT_TEST,
    DATABASE_CONFIG
)

DB_URL = f'postgres://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}'


async def init_db(command) -> None:
    """Initial database connection"""
    await command.init_db(safe=True)


async def init(command):
    try:
        await init_db(command)
    except:
        pass


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    res = policy.new_event_loop()
    asyncio.set_event_loop(res)
    res._close = res.close
    res.close = lambda: None
    yield res
    res._close()


@pytest.fixture(scope="module")
async def client():
    async with httpx.AsyncClient(base_url="http://testserver:8000", app=app) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    DATABASE_CONFIG['connections']['default'] = DB_URL
    command = Command(
        app='cargo',
        tortoise_config=DATABASE_CONFIG,
        location='./tests/migrations'
    )
    await command.init()
    await init(command)

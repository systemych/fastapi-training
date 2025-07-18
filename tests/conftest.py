# ruff: noqa: E402

import json
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest
from httpx import AsyncClient, ASGITransport

from src.main import app
from src.api.dependencies.db_manager import get_db_manager
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.utils.db_manager import DBManager
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAddRequest
from src.models import *  # noqa


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="session")
async def db() -> DBManager:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db_manager] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        with open("tests\mock_hotels.json", encoding="utf-8") as f:
            content = f.read()
            for hotel in json.loads(content):
                await db.hotels.add(HotelAdd(**hotel))
        with open("tests\mock_rooms.json", encoding="utf-8") as f:
            content = f.read()
            for room in json.loads(content):
                await db.rooms.add(RoomAddRequest(**room), exclude_unset=True)

        await db.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def create_user(ac, setup_database):
    await ac.post(
        "/auth/register", json={"email": "ivanov@company.com", "password": "qwerty"}
    )


@pytest.fixture(scope="session", autouse=True)
async def auth_ac(create_user, ac) -> AsyncClient:
    await ac.post(
        "/auth/login", json={"email": "ivanov@company.com", "password": "qwerty"}
    )
    yield ac

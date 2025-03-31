from collections.abc import AsyncIterator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport
from httpx import AsyncClient

from app.api import init_app
from app.config import get_config


pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return init_app(config=get_config())


@pytest.fixture(scope="function")
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

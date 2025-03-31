import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_healthcheck(client: AsyncClient) -> None:
    response = await client.get("/health/")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json() == {"status": True}

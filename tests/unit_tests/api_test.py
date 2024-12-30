import pytest
from httpx import AsyncClient



@pytest.mark.asyncio
async def test_add_links(ac: AsyncClient):
    response = await ac.post(url="/visited_links", json={
    "links": [
        "https://example.com",
        "python.org",
        "https://stackoverflow.com/questions",
        "https://github.com",
        "apple.com"
        ]
    })
    response_json = response.json()
    assert response_json["status"] == 200

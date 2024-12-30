import json

import pytest
import fakeredis

from fastapi.testclient import TestClient
from httpx import AsyncClient
from src.main import app as fastapi_app


@pytest.fixture(scope="session", autouse=True)
def prepare_db():
    redis = fakeredis.FakeStrictRedis()

    redis.flushdb(asynchronous=True)

    def open_mock_json(model: str):
        with open(f"tests/mock_data_{model}.json", encoding='utf-8') as file:
            return json.load(file)

    request = open_mock_json("links")

    counter = 0

    for link in request:
        key = f"hd{counter}"
        data = {
            "links": json.dumps(link["links"]),
            "time": link["time"],
        }

        redis.hset(key, mapping=data)
        counter += 1

    print(redis.hgetall(f"hd0"))


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(base_url='http://127.0.0.1:8000') as ac:
        yield ac
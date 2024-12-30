from datetime import datetime
from typing import Dict

from fastapi import FastAPI
from starlette.requests import Request

from fastapi_cache.decorator import cache
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.models import LinksResponse, DomainsResponse, LinksRequest
from src.controllers import add_links, get_domains_by_time

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from src.db_connection import redis

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    if redis:
        print("connected to redis")
    yield


app = FastAPI(lifespan=lifespan)


@app.post('/visited_links')
async def get_links(request: LinksRequest) -> LinksResponse:
    return await add_links(request=request)


@app.get('/visited_domains')
async def get_domains(date_from: int, date_to: int) -> DomainsResponse:
    return await get_domains_by_time(date_from=date_from, date_to=date_to)

@app.get('/generate_data')
async def generate():
    for i in range(10000):
        await redis.set(i, f'{i}+abc')
    return "all good man"
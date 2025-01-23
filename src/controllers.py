import json

import redis.exceptions as r
from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from src.Services.domains import validate_urls_by_time, get_domains_from_urls
from src.Services.keys import get_last_id, get_all_keys
from src.db_connection import redis
from src.models import LinksRequest, LinksResponse, DomainsResponse



async def add_links(request: LinksRequest) -> LinksResponse:
    if not request:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="empty request")

    data_received_time = int(datetime.timestamp(datetime.now()))

    data = {
        "links": json.dumps(request.links),
        "time": data_received_time
    }

    try:
        new_id = await get_last_id()+1
        await redis.hset(f"hd{new_id}", mapping=data)

    except r.ConnectionError as e:
        print(f"Connection error {e}")
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="connection error")
    except r.DataError as e:
        print(f"Data error {e}")
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="invalid data error")
    except Exception as e:
        print(f"Unknown error {e}")
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="unexpected error")


    return LinksResponse(links=request.links, status=HTTPStatus.OK)


async def get_domains_by_time(date_from: int, date_to: int) -> DomainsResponse:
    if date_from > date_to:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="wrong date")

    keys = await get_all_keys()

    urls = await validate_urls_by_time(keys, date_from, date_to)

    domains_by_time = get_domains_from_urls(urls)
    return DomainsResponse(domains=domains_by_time, status=HTTPStatus.OK)


from datetime import datetime
from http import HTTPStatus
from typing import List

from pydantic import BaseModel, Field


class LinksRequest(BaseModel):
    links: List[str]


class LinksResponse(BaseModel):
    links: List[str]
    status: HTTPStatus


class DomainsResponse(BaseModel):
    domains: List[str]
    status: HTTPStatus
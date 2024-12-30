from collections import OrderedDict
from urllib.parse import urlparse

from src.db_connection import redis


def get_domains_from_urls(urls: list) -> list:
    domains = OrderedDict()

    for url in urls:
        if '://' not in url:
            url = 'http://' + url

        domains[urlparse(url).netloc] = None

    return list(domains.keys())


async def validate_urls_by_time(keys: list, date_from: int, date_to: int):
    validated_urls = []
    for key in keys:
        time = await redis.hget(key, "time")
        timestamp = int(time.decode('utf-8'))

        if date_from <= timestamp <= date_to:

            urls = await redis.hget(key, "links")
            validated_urls.extend(urls.decode("utf-8")[1:-1].replace(' ', '').replace('"', '').split(','))

    return validated_urls
from src.db_connection import redis


async def get_all_keys():
    keys = []
    cursor = 0

    while True:
        cursor, partial_keys = await redis.scan(cursor=cursor)
        keys.extend(partial_keys)

        if cursor == 0:
            break

    return keys


async def get_last_id():
    keys = await get_all_keys()
    max_id = -1

    for key in keys:
        key = key.decode('utf8')
        if max_id < int(key[2::]):
            max_id = int(key[2::])

    return max_id
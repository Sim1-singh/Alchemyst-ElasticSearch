import os

import aiohttp

BASE_URL = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")

if BASE_URL.endswith("/"):
    BASE_URL = BASE_URL[:-1]

GLOBAL_CLIENT: aiohttp.ClientSession = aiohttp.ClientSession(
    base_url=BASE_URL, conn_timeout=30.0
)


async def get_client() -> aiohttp.ClientSession:
    global GLOBAL_CLIENT
    if GLOBAL_CLIENT.closed:
        GLOBAL_CLIENT = aiohttp.ClientSession(base_url=BASE_URL, conn_timeout=30.0)
    return GLOBAL_CLIENT

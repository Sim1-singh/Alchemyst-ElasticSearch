"""Client for making requests to the backend"""

from typing import Any, Dict, Literal

import aiohttp
from client.settings import get_client


async def request(
    endpoint: str,
    method: Literal["GET", "POST", "PATCH", "PUT", "DELETE", "HEAD", "OPTIONS"] = "GET",
    logs: Dict[str, Any] = {},
    **kwargs,
) -> Dict[str, Any]:
    """Make a request to the backend"""
    # TODO: Implement this function
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint

    client = await get_client()
    async with client:
        response = await client.request(
            method=method, url=endpoint, json=kwargs.get("data")
        )

        print(response.status)
        url = response.url
        print(url)
        resp = await response.json()
        print(resp)

        return resp


async def bulk_request(endpoint: str, method="POST", **kwargs):
    """Make a request to the backend"""
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint

    client = get_client()
    async with client:
        response = await client.request(method=method, url=endpoint, **kwargs)

        print(response.status_code)
        resp = response.json()
        print(resp)

        return resp


if __name__ == "__main__":  # Test code
    import asyncio

    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(request("/careers"))
    print(res)
    loop.close()

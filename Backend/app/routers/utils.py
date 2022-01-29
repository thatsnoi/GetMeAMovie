from aiohttp.client import ClientSession
from typing import Dict

async def async_request(session: ClientSession, url: str, params: Dict[str, str]):
    async with session.get(url, params=params) as response:
        # Return JSON only if the information has been found
        if response.status == 200:
            return await response.json()

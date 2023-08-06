from http.client import HTTPSConnection
from base64 import b64encode
from json import loads
from json import dumps
import aiohttp
import asyncio
import async_timeout


class RestClient:
    domain = "api.dataforseo.com"

    def __init__(self, username, password):
        self.username = username
        self.password = password

    async def request(self, path, method, data=None):
        async with aiohttp.ClientSession() as session:
            url = f"https://{self.domain}{path}"
            headers = {
                'Authorization': f'Basic {b64encode(f"{self.username}:{self.password}".encode()).decode()}',
                'Content-Encoding': 'gzip'
            }
            async with async_timeout.timeout(10):
                async with session.request(method, url, headers=headers, data=data) as response:
                    return await response.json()

    async def get_async(self, path):
        return await self.request(path, 'GET')

    async def post_async(self, path, data):
        if isinstance(data, str):
            data_str = data
        else:
            data_str = dumps(data)
        return await self.request(path, 'POST', data_str)

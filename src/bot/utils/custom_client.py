import aiohttp
from aiohttp import ClientResponse

from src.configuration import conf
from src.cache.adapter import Cache


class Client:
    def __init__(self):
        self.cache = Cache()
        self.session = aiohttp.ClientSession()

    async def __aenter__(self):
        access_key = await self.get_access_token()
        self.session.headers.setdefault("Authorization", f"Bearer {access_key}")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def update_access_token(self, access_token):
        await self.cache.set("ACCESS_TOKEN", access_token)
    
    async def get_access_token(self):
        access_token = await self.cache.get("ACCESS_TOKEN")
        if not access_token:
            await self.login()
            return await self.get_access_token()
        return access_token.decode()
    
    async def login(self):
        url = 'https://api-admin.billz.ai/v1/auth/login'
        payload = {"secret_token": conf.BILLZ_SECRET_KEY}

        async with self.session.post(url, json=payload) as response:
            data = await response.json()
            access_token = data.get('data').get('access_token')
            await self.update_access_token(access_token)
            self.session.headers.update({"Authorization": f"Bearer {access_token}"})

    async def post(self, url: str, payload: dict) -> ClientResponse:
        async with self.session.post(url, json=payload) as response:
            status = response.status
            print("response status:", status)
            print("response json:", await response.json())
            if response.status == 401:
                await self.login()
                return await self.post(url, payload)
            
            return await response.json()

    async def get(self, url: str) -> ClientResponse:
        async with self.session.get(url) as response:
            if response.status == 401:
                await self.login()
                return await self.get(url)
            
            return await response.json()


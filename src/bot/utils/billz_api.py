import aiohttp

from typing import Optional
from aiohttp import ClientResponse

from src.configuration import conf


class BillzAPI:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {conf.BILLZ_API_KEY}"
        }

    async def post(self, url: str, payload: str) -> ClientResponse:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    access_token = await self.login()
                    self.headers['Authorization'] = f"Bearer {access_token}"
                    return await self.post(url, payload)
                
                return response
            
    async def get(self, url: str) -> ClientResponse:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    access_token = await self.login()
                    self.headers['Authorization'] = f"Bearer {access_token}"
                    return 

                return response
            
    async def login(self):
        url = 'https://api-admin.billz.ai/v1/auth/login'

        payload = {
            "secret_token": conf.BILLZ_SECRET_KEY
        }

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(url, json=payload) as response:
                data = await response.json()
                return data

        response: ClientResponse = await self.post(url, payload)
        data: dict = await response.json()
        access_token = data.get('data').get('access_token')
        return access_token
            
    async def set_user(
        self, 
        chat_id: str, 
        first_name: str, 
        last_name: str, 
        phone_number: str, 
        date_of_birth: Optional[str] = '2022-05-14',
        gender: Optional[int] = 1,
    ):
        url = 'https://api-admin.billz.ai/v1/client'
        payload = {
            "chat_id": chat_id,
            "date_of_birth": date_of_birth,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "gender": gender
        }

        # response = await self.post(url, payload)
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    access_token = await self.login()
                    self.headers['Authorization'] = f"Bearer {access_token}"

                data = await response.json()
                return data     

    async def get_user(self, chat_id: int):
        url = f'https://api-admin.billz.ai/v1/client?chat_id={chat_id}'
        
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    access_token = await self.login()
                    self.headers['Authorization'] = f"Bearer {access_token}"

                data: dict = await response.json()

                if data.get('clients'):
                    return data.get('clients')[0]
            
    async def add_item(self, order_id: str, product_id: str, count: int):
        url = 'https://api-admin.billz.ai/v1/orders'
        payload = {
            "method": "order.add_item",
            "params": {
                "product_id": product_id,
                "measurement_value": count,
                "order_id": order_id
            }
        }

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(url, json=payload) as response:
                # print(await response.text())
                # if response.status != 200:
                #     access_token = await self.login()
                #     self.headers['Authorization'] = f"Bearer {access_token}"

                # response = await self.post(url, payload)
                data = await response.json()  # Parse JSON response
                return data

    async def make_payment(self, order_id: str, total_amount: int):
        url = 'https://api-admin.billz.ai/v1/orders'
        payload = {
            "method": "order.make_payment",
            "params": {
                "payments": [
                    {
                        "id": "61f8f3f8-979e-4316-b830-b01482121429",
                        "company_payment_type_id": "e506cdb9-eddc-4ada-9ba6-b124fba2f917", # static
                        "paid_amount": total_amount
                    }
                ],
                "order_id": order_id
            }
        }

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(url, json=payload) as response:
                data = await response.json()  # Parse JSON response
                return data

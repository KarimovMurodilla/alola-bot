import aiohttp
from src.configuration import conf


class BillzAPI:
    def __init__(self):
        self.headers = {
            "Authorization": conf.BILLZ_API_KEY
        }
            
    async def set_user(self, chat_id: str, first_name: str, last_name: str, phone_number: str):
        url = 'https://api-admin.billz.ai/v1/client'
        payload = {
            "chat_id": chat_id,
            "date_of_birth": "2022-05-14",
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "gender": 0
        }
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(url, json=payload) as response:
                print(f"Status: {response.status}")
                data = await response.json()  # Parse JSON response
                return data     

    async def get_user(self, phone_number: str):
        url = f'https://api-admin.billz.ai/v1/client?phone_number={phone_number}'
        
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
                print(f"Status: {response.status}")
                data = await response.json()
                return data

import aiohttp
import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

storage=MemoryStorage()

TOKEN = str(os.getenv("TOKEN"))

URL_APP = 'https://deplbot-0e88a7540a4d.herokuapp.com/'

POSTGREURI = str(os.getenv("DATABASE_URL"))

# ip=os.getenv("ip")
ip = 'localhost'
operator = 6398627453
admin = 2006308022
sender_photo = 6366939865
arenda_items = ['59']

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

url_webhook = 'https://vostoktekhgaz.bitrix24.kz/rest/4053/zke9kazjd7b4eeub/'
method = 'crm.lead.add'
method2 ='crm.lead.productrows.set'

async def b24rest_request(url_webhook: str, method: str, parametr: dict) -> dict:
    url = url_webhook + method + '.json?'
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=parametr) as response:
            response_data = await response.json()
            if response.status == 200:
                # Запрос выполнен успешно
                print(f"Ответ сервера: {response_data}")
            else:
                print(f"Ошибка при выполнении запроса. Статус код: {response_data}") 
    return response_data
    # response = requests.post(url, verify=False, json=parametr)
    # print(response) 
    # return response.json()

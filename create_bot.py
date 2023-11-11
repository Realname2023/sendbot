# import requests
import aiohttp
import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

storage=MemoryStorage()

TOKEN = str(os.getenv("TOKEN"))
# TOKEN = '6684662073:AAGw6gZtBmQ0QWpoRnvoyAsZeswyDUQipnw'

URL_APP = 'https://deplbot-0e88a7540a4d.herokuapp.com/'

POSTGREURI = str(os.getenv("DATABASE_URL"))

# ip=os.getenv("ip")
ip = 'localhost'
# PGUSER=str(os.getenv("PGUSER"))
# PGUSER = 'postgres'
# PGPASSWORD = str(os.getenv("PGPASSWORD"))
# PGPASSWORD = 'cont2023'
# DATABASE = str(os.getenv("DATABASE"))
# DATABASE = 'vostok'
# POSTGREURI=f'postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}'
# POSTGREURI = 'postgres://oudkamoyueapuv:26ce0912ff0ce412bd22fdce6c0111954f42076a9af30010ad01e0fa2a8fd633@ec2-34-242-154-118.eu-west-1.compute.amazonaws.com:5432/d8sr8luiviue8r'
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

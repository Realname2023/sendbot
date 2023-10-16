from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

storage=MemoryStorage()

# TOKEN = str(os.getenv("TOKEN"))
TOKEN = '6684662073:AAGw6gZtBmQ0QWpoRnvoyAsZeswyDUQipnw'

URL_APP = 'https://deplbot-a5f641a62530.herokuapp.com/'

# ip=os.getenv("ip")
ip = 'localhost'
# PGUSER=str(os.getenv("PGUSER"))
# PGUSER = 'postgres'
# PGPASSWORD = str(os.getenv("PGPASSWORD"))
# PGPASSWORD = 'cont2023'
# DATABASE = str(os.getenv("DATABASE"))
# DATABASE = 'vostok'
# POSTGREURI=f'postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}'
POSTGREURI = 'postgres://oudkamoyueapuv:26ce0912ff0ce412bd22fdce6c0111954f42076a9af30010ad01e0fa2a8fd633@ec2-34-242-154-118.eu-west-1.compute.amazonaws.com:5432/d8sr8luiviue8r'
operator = 6398627453

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
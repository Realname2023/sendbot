from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

storage=MemoryStorage()

# TOKEN = str(os.getenv("TOKEN"))
TOKEN = '6684662073:AAGw6gZtBmQ0QWpoRnvoyAsZeswyDUQipnw'

# ip=os.getenv("ip")
ip = 'localhost'
# PGUSER=str(os.getenv("PGUSER"))
PGUSER = 'postgres'
# PGPASSWORD = str(os.getenv("PGPASSWORD"))
PGPASSWORD = 'cont2023'
# DATABASE = str(os.getenv("DATABASE"))
DATABASE = 'vostok'
POSTGREURI=f'postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}'
operator = 6398627453

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
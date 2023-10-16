import os
from aiogram.utils import executor
from create_bot import dp, URL_APP, bot
from data_base.gino_db import db, db_startup
import logging

logging.basicConfig(level=logging.INFO)

async def on_startup(dp):
    import middlewares
    await bot.set_webhook(URL_APP)
    middlewares.setup(dp)
    print('Бот вышел в онлайн')
    print('Connecting to POSTGRESQL')
    await db_startup(dp)
    # # print('Очистка таблиц')
    # # await db.gino.drop_all()
    print('Сшздание таблиц')
    await db.gino.create_all()
    print('Готово')

async def on_shutdown(dp):
    await bot.delete_webhook()

from handlers import client, admin

# client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
# other.register_handlers_other(dp)

# executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
executor.start_webhook(
    dispatcher=dp,
    webhook_path='',
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    skip_updates=True,
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 5000))
)

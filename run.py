import os
import logging
from aiogram.utils import executor
from create_bot import dp, URL_APP, bot
from data_base.gino_db import db, db_startup
from handlers import admin, client, buy, inline, order, admin_cat, admin_import

logging.basicConfig(level=logging.INFO)

async def on_startup(dp):
    import middlewares
    await bot.set_webhook(URL_APP)
    middlewares.setup(dp)
    print('Бот вышел в онлайн')
    print('Connecting to POSTGRESQL')
    await db_startup(dp)
    print('Сшздание таблиц')
    await db.gino.create_all()
    print('Готово')

async def on_shutdown(dp):
    await bot.delete_webhook()


admin.register_handlers_admin(dp)
admin_cat.register_handlers_admin_cat(dp)
admin_import.register_handlers_admin_import(dp)
client.register_handlers_client(dp)
buy.register_handlers_buy(dp)
inline.register_handlers_inline(dp)
order.register_handlers_order(dp)

executor.start_webhook(
    dispatcher=dp,
    webhook_path='',
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    skip_updates=True,
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 5000))
)

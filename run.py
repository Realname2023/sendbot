from aiogram.utils import executor
from create_bot import dp
from data_base.gino_db import db, db_startup
import logging

logging.basicConfig(level=logging.INFO)

async def on_startup(_):
    import middlewares
    middlewares.setup(dp)
    print('Бот вышел в онлайн')
    print('Connecting to POSTGRESQL')
    await db_startup(dp)
    # print('Очистка таблиц')
    # await db.gino.drop_all()
    print('Сшздание таблиц')
    await db.gino.create_all()
    print('Готово')



from handlers import client, admin

# client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
# other.register_handlers_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


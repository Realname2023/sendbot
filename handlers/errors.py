from aiogram import types
from aiogram.utils.exceptions import *
from create_bot import dp, bot
from keyboards.client_kb import kb_client

@dp.errors_handler()
async def errors(update: types.Update, exception):
    print(update)
    if update.message:
        user = update.message["from"]["id"]
        await bot.send_message(user, "Ошибка сервера. Выберите товары", reply_markup=kb_client)
    if update.callback_query:
        user = update.callback_query["from"]["id"]
        await bot.send_message(user, "Ошибка сервера. Выберите товары", reply_markup=kb_client)
    return True

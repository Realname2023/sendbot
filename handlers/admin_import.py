from aiogram import types, Dispatcher
from create_bot import bot, admin
from keyboards import admin_kb
from data_base.base_db import Category


# @dp.message_handler(commands=['moderator3'], is_chat_admin=True)
async def make_changes_command_import(message : types.Message):
    if message.from_user.id == admin:
        await bot.send_message(message.from_user.id, 'Что хозяин надо???', reply_markup=admin_kb.button_case_admin)
        await message.delete()

# @dp.message_handler(commands=['Загрузка_из_файла'])
async def load_from_file(message: types.Message):
    if message.from_user.id == admin:
        with open("category.txt", "r", encoding="UTF8") as file:
            f = file.readlines()
            for i in f:
                m = i.split("\t")
                id = int(m[0])
                row_width = int(m[3])
                data = m[5].replace("\n", "")
                print(m)
                cat = Category(id=id, callback=m[1], edit_text=m[2], row_width=row_width, button_text=m[4], button_data=data)
                await cat.create()
    await message.answer('Категория успешно загружены')

def register_handlers_admin_import(dp: Dispatcher):
    dp.register_message_handler(load_from_file, commands=['Загрузка_из_файла'])
    dp.register_message_handler(make_changes_command_import, commands=['moderator3'], is_chat_admin=True)

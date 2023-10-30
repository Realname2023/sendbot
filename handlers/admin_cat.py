from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from create_bot import bot
from handlers.states import FSMAdmin2
from keyboards import admin_kb
from data_base.base_db import Category

ID = None


# @dp.message_handler(commands=['moderator2'], is_chat_admin=True)
async def make_changes_command_cat(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(
        message.from_user.id,
        "Что хозяин надо???",
        reply_markup=admin_kb.button_case_admin,
    )
    await message.delete()


# @dp.message_handler(commands=['Загрузить_категорию'], state=None)
async def cat_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin2.id.set()
        await message.reply("Укажи id")


# @dp.message_handler(state=FSMAdmin2.id)
async def set_id(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        id = int(message.text)
        await state.update_data(id=id)
        await message.reply("Теперь укажи callback")
        await FSMAdmin2.callback.set()


# @dp.message_handler(state=FSMAdmin2.callback)
async def set_callback(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        callback = message.text
        await state.update_data(callback=callback)
        await message.reply("Теперь укажи edit_text")
        await FSMAdmin2.edit_text.set()


# @dp.message_handler(state=FSMAdmin2.edit_text)
async def set_edit_text(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        edit_text = message.text
        await state.update_data(edit_text=edit_text)
        await message.reply("Теперь укажи row_width")
        await FSMAdmin2.row_width.set()


# @dp.message_handler(state=FSMAdmin2.row_width)
async def set_row_width(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        row_width = int(message.text)
        await state.update_data(row_width=row_width)
        await message.reply("Теперь укажи button_text")
        await FSMAdmin2.button_text.set()


# @dp.message_handler(state=FSMAdmin2.button_text)
async def set_button_text(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        button_text = message.text
        await state.update_data(button_text=button_text)
        await message.reply("Теперь укажи button_data")
        await FSMAdmin2.button_data.set()


# @dp.message_handler(state=FSMAdmin2.button_data)
async def set_button_data(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        button_data = message.text
        await state.update_data(button_data=button_data)
        data = await state.get_data()
        id = data.get("id")
        callback = data.get("callback")
        edit_text = data.get("edit_text")
        row_width = data.get("row_width")
        button_text = data.get("button_text")
        button_data = data.get("button_data")
        cat = Category(
            id=id,
            callback=callback,
            edit_text=edit_text,
            row_width=row_width,
            button_text=button_text,
            button_data=button_data,
        )
        await cat.create()
        await state.reset_state()


def register_handlers_admin_cat(dp: Dispatcher):
    dp.register_message_handler(cat_start, commands=["Загрузить_категорию"], state=None)
    dp.register_message_handler(set_id, state=FSMAdmin2.id)
    dp.register_message_handler(set_callback, state=FSMAdmin2.callback)
    dp.register_message_handler(set_edit_text, state=FSMAdmin2.edit_text)
    dp.register_message_handler(set_row_width, state=FSMAdmin2.row_width)
    dp.register_message_handler(set_button_text, state=FSMAdmin2.button_text)
    dp.register_message_handler(set_button_data, state=FSMAdmin2.button_data)
    dp.register_message_handler(
        make_changes_command_cat, commands=["moderator2"], is_chat_admin=True
    )

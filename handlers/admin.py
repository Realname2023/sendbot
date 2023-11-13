from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from create_bot import bot, admin
from handlers.states import FSMAdmin
from keyboards import admin_kb
from data_base.base_db import All_items


# Получаем id текущего модератора
# @dp.message_handler(commands=["moderator"], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    if message.from_user.id == admin:
        await bot.send_message(
            message.from_user.id,
            "Что хозяин надо???",
            reply_markup=admin_kb.button_case_admin,
        )
        await message.delete()


# Начало диалога загрузки первого пункта меню
# @dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == admin:
        await FSMAdmin.photo.set()
        await message.reply("Загрузи фото")


# Выход из состояний
# @dp.message_handler(Text(equals='отмена_загрузки', ignore_case=True), state="*")
# @dp.message_handler(state="*", commands=['отмена_загрузки'])
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == admin:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply("Ok")


# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == admin:
        photo = message.photo[-1].file_id
        await message.reply("Теперь введи id")
        await FSMAdmin.item_id.set()
        await state.update_data(photo=photo)


# @dp.message_handler(state=FSMAdmin.item_id)
async def load_id(message: types.Message, state: FSMContext):
    if message.from_user.id == admin:
        item_id = message.text
        await message.reply("Теперь укажи название")
        await FSMAdmin.name.set()
        await state.update_data(item_id=item_id)



# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == admin:
        name = message.text
        await message.reply("Введи единицу измерения")
        await FSMAdmin.unit.set()
        await state.update_data(name=name)


# @dp.message_handler(state=FSMAdmin.unit)
async def load_unit(message: types.Message, state: FSMContext):
    if message.from_user.id == admin:
        unit = message.text
        await message.reply("Введи описание")
        await FSMAdmin.description.set()
        await state.update_data(unit=unit)


# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == admin:
        description = message.text
        await message.reply("Теперь укажи цену")
        await FSMAdmin.price.set()
        await state.update_data(description=description)


# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == admin:
        price = int(message.text)
        await message.reply("Теперь укажи цену с доставкой")
        await FSMAdmin.del_price.set()
        await state.update_data(price=price)

# @dp.message_handler(state=FSMAdmin.del_price)
async def load_del_price(message: types.Message, state: FSMContext):
    if message.from_user.id == admin:
        del_price = int(message.text)
        await message.reply("Теперь укажи склад")
        await FSMAdmin.item_city.set()
        await state.update_data(del_price=del_price)

# @dp.message_handler(state=FSMAdmin.item_city)
async def load_city(message: types.Message, state: FSMContext):
    if message.from_user.id == admin:
        item_city = message.text
        await message.reply("Теперь укажи cat_back")
        await FSMAdmin.cat_back.set()
        await state.update_data(item_city=item_city)

# @dp.message_handler(state=FSMAdmin.cat_back)
async def load_cat_back(message: types.Message, state: FSMContext):
    if message.from_user.id == admin:
        cat_back = message.text
        data = await state.get_data()
        photo = data.get("photo")
        item_id = data.get("item_id")
        name = data.get("name")
        unit = data.get("unit")
        description = data.get("description")
        price = data.get("price")
        del_price= data.get("del_price")
        item_city = data.get("item_city")
        item = All_items(item_id=item_id, photo=photo, name=name, unit=unit, 
                         description=description, price=price, del_price=del_price,
                         city=item_city, city_back=cat_back)
        await item.create()
        await state.reset_state()


# Регистрируем хендлеры
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=["Загрузить"], state=None)
    dp.register_message_handler(
        cancel_handler, Text(equals="отмена_загрузки", ignore_case=True), state="*"
    )
    dp.register_message_handler(
        load_photo, content_types=["photo"], state=FSMAdmin.photo
    )
    dp.register_message_handler(load_id, state=FSMAdmin.item_id)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_unit, state=FSMAdmin.unit)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(load_del_price, state=FSMAdmin.del_price)
    dp.register_message_handler(load_city, state=FSMAdmin.item_city)
    dp.register_message_handler(load_cat_back, state=FSMAdmin.cat_back)
    dp.register_message_handler(
        make_changes_command, commands=["moderator"], is_chat_admin=True
    )

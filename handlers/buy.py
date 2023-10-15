from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot, operator
from data_base.base_db import Client, CurrentOrder
from handlers import quick_commands as commands
from handlers.order import create_order
from handlers.states import buy_item, FSMClient, get_order
from keyboards import cancel_buy_kb, kb_client, order_kb
from aiogram.types import ReplyKeyboardRemove
import re


@dp.message_handler(state="*", commands=['отмена'])
async def cancel_handier(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer('Ok', reply_markup=ReplyKeyboardRemove())
        await message.answer('Выберите товары', reply_markup=kb_client)
        return
    await state.finish()
    await message.answer('Ok', reply_markup=ReplyKeyboardRemove())
    await message.answer('Выберите товары', reply_markup=kb_client)


@dp.callback_query_handler(buy_item.filter())
async def callback_buy(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user = call.from_user.id
    item_id = callback_data.get("item_id")
    price = int(callback_data.get("price"))
    read = await commands.select_item(item_id)
    item = read.name
    unit = read.unit
    city = read.city
    await call.answer(text=f'Укажите количество {unit} {item}.', show_alert=True)
    await call.message.edit_reply_markup()
    await bot.send_message(user, text=f"Укажие количество {unit} {item}", reply_markup=cancel_buy_kb)
    await FSMClient.buy_quantity.set()
    await state.update_data(buy_item_id=item_id)
    await state.update_data(item=item)
    await state.update_data(buy_price=price)
    await state.update_data(buy_unit=unit)
    await state.update_data(city=city)


@dp.message_handler(state=FSMClient.buy_quantity)
async def load_quantity(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    pat = r"[^0-9]"
    answer = re.sub(pat, "", message.text)
    try:
        answer = int(answer)
    except ValueError:
        await message.answer("Укажите количество в цифрах")
        return
    await state.update_data(buy_quantity=answer)
    client = await commands.select_client(user_id)
    if client == None:
        await message.answer("Укажите нименование Вашей организации  если Вы физ лицо, то напишите как к Вам обращаться")
        await FSMClient.org_name.set()
    else:
        data = await state.get_data()
        item_id = data.get("buy_item_id")
        name = data.get('item')
        price = data.get('buy_price')
        quantity = int(data.get('buy_quantity'))
        unit = data.get("buy_unit")
        sum = price * quantity
        city = data.get("city")
        comment = ''
        await commands.add_current_order(user_id, item_id, name, unit, price, quantity, sum, city, comment)
        await state.finish()
        await create_order(user_id, message)


@dp.message_handler(state=FSMClient.org_name)
async def indicate_org(message: types.Message, state: FSMContext):
    org_name = message.text
    await state.update_data(org_name=org_name)
    await message.answer("Укажите адрес доставки")
    await FSMClient.address.set()


@dp.message_handler(state=FSMClient.address)
async def indicate_address(message: types.Message, state: FSMContext):
    address = message.text
    await state.update_data(address=address)
    await message.answer("Укажите Ваш номер телефона")
    await FSMClient.phone.set()


@dp.message_handler(state=FSMClient.phone)
async def indicate_phone(message: types.Message, state: FSMContext):
    phone = message.text
    user_id = message.from_user.id
    data = await state.get_data()
    city = data.get("city")
    org_name = data.get("org_name")
    address = data.get("address")
    client = Client(user_id=user_id, city=city, org_name=org_name, address=address,
                    phone=phone)
    await client.create()
    item_id = data.get("buy_item_id")
    name = data.get('item')
    price = data.get('buy_price')
    quantity = int(data.get('buy_quantity'))
    unit = data.get("buy_unit")
    sum = price * quantity
    comment = ''
    await state.finish()
    await commands.add_current_order(user_id, item_id, name, unit, price, quantity, sum, city, comment)
    await create_order(user_id, message)

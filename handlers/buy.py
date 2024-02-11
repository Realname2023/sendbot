import re
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from create_bot import bot, arenda_items, arenda_eq
from data_base.base_db import Client
from handlers import quick_commands as commands
from handlers.order import create_order
from handlers.states import buy_item, FSMClient
from keyboards import cancel_buy_kb, kb_client, phone_button_kb
from aiogram.types import ReplyKeyboardRemove, ContentTypes


# @dp.message_handler(state="*", commands=['отмена'])
async def cancel_buy(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer('Ok', reply_markup=ReplyKeyboardRemove())
        await message.answer('Выберите товары и создайте заказ', reply_markup=kb_client)
        return
    await state.finish()
    await message.answer('Ok', reply_markup=ReplyKeyboardRemove())
    await message.answer('Выберите товары и создайте заказ', reply_markup=kb_client)


# @dp.callback_query_handler(buy_item.filter())
async def callback_buy(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user = call.from_user.id
    item_id = callback_data.get("item_id")
    price = int(callback_data.get("price"))
    read = await commands.select_item(item_id)
    item = read.name
    unit = read.unit
    city = read.city
    b_id = read.b_id
    await call.answer(text=f'Укажите количество {unit} {item}.', show_alert=True)
    await call.message.edit_reply_markup()
    await bot.send_message(user, text=f"Укажите количество {unit} {item}", reply_markup=cancel_buy_kb)
    await FSMClient.buy_quantity.set()
    await state.update_data(buy_item_id=item_id)
    await state.update_data(buy_b_id=b_id)
    await state.update_data(item=item)
    if price == read.del_price:
        await state.update_data(buy_del_price=price)
        await state.update_data(buy_price=read.price)
        await state.update_data(delivery=1)
    else:
        await state.update_data(buy_price=price)
        await state.update_data(buy_del_price=read.del_price)
        await state.update_data(delivery=0)
    await state.update_data(buy_unit=unit)
    await state.update_data(city=city)


# @dp.message_handler(state=FSMClient.buy_quantity)
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
    data = await state.get_data()
    item_id = data.get("buy_item_id")
    delivery = data.get("delivery")
    name = data.get('item')
    if (item_id in arenda_items and delivery == 1) or item_id in arenda_eq:
        await message.answer(f"Укажите на сколько месяцев Вы арендуете {name}")
        await FSMClient.buy_arenda_time.set()
    elif client is None:
        await message.answer("Укажите нименование Вашей организации  если Вы физ лицо, то напишите как к Вам обращаться")
        await FSMClient.org_name.set()
    else:
        b_id = data.get("buy_b_id")
        user_item = str(user_id) + item_id
        price = data.get('buy_price')
        del_price = data.get('buy_del_price')
        quant = int(data.get('buy_quantity'))
        unit = data.get("buy_unit")
        delivery = data.get("delivery")
        arenda_time = 0
        del_quantity = 0
        quantity = 0
        if delivery == 1:
            del_quantity = quant
            sum = del_price * quant
        else:
            quantity = quant
            sum = price * quant
        city = data.get("city")
        comment = ''
        await commands.add_current_order(user_item, user_id, item_id, b_id, name, 
                                         unit, price, del_price, quantity, 
                                         del_quantity, arenda_time,
                                         sum, city, comment)
        await state.finish()
        await create_order(user_id)


# @dp.message_handler(state=FSMClient.buy_arenda_time)
async def indicate_arenda_time(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    pat = r"[^0-9]"
    answer = re.sub(pat, "", message.text)
    try:
        answer = int(answer)
    except ValueError:
        await message.answer("Укажите время аренды в цифрах")
        return
    await state.update_data(buy_arenda_time=answer)
    client = await commands.select_client(user_id)
    if client is None:
        await message.answer("Укажите наименование Вашей организации. Если Вы физ.лицо, то напишите, как к Вам обращаться.")
        await FSMClient.org_name.set()
    else:
        data = await state.get_data()
        item_id = data.get("buy_item_id")
        b_id = data.get("buy_b_id")
        name = data.get('item')
        user_item = str(user_id) + item_id
        price = data.get('buy_price')
        del_price = data.get('buy_del_price')
        del_quantity = int(data.get('buy_quantity'))
        arenda_time = int(data.get("buy_arenda_time"))
        unit = data.get("buy_unit")
        quantity = 0
        city = data.get("city")
        delivery = data.get("delivery")
        comment = ''
        if item_id in arenda_eq and delivery == 0:
            quantity = del_quantity
            del_quantity = 0
            sum = price*quantity*arenda_time
        else:
            sum = del_price*del_quantity*arenda_time
        await commands.add_current_order(user_item, user_id, item_id, b_id, name, unit,
                                         price, del_price, quantity, del_quantity,
                                         arenda_time, sum, city, comment)
        await state.finish()
        await create_order(user_id)


# @dp.message_handler(state=FSMClient.org_name)
async def indicate_org(message: types.Message, state: FSMContext):
    org_name = message.text
    await state.update_data(org_name=org_name)
    await message.answer("Укажите адрес доставки")
    await FSMClient.address.set()


# @dp.message_handler(state=FSMClient.address)
async def indicate_address(message: types.Message, state: FSMContext):
    address = message.text
    await state.update_data(address=address)
    await message.answer("Для обратной связи поделитесь контактом. Нажмите /Поделиться_контактом", 
                         reply_markup=phone_button_kb)
    await FSMClient.phone.set()


# @dp.message_handler(state=FSMClient.phone)
async def indicate_phone(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    user_id = message.from_user.id
    user_name = message.from_user.username
    full_name = message.from_user.full_name
    data = await state.get_data()
    city = data.get("city")
    org_name = data.get("org_name")
    address = data.get("address")
    client = Client(user_id=user_id, city=city, org_name=org_name, address=address,
                    phone=phone, user_name=user_name, full_name=full_name)
    await client.create()
    item_id = data.get("buy_item_id")
    b_id = data.get("buy_b_id")
    user_item = str(user_id) + item_id
    name = data.get('item')
    price = data.get('buy_price')
    del_price = data.get('buy_del_price')
    quant = int(data.get('buy_quantity'))
    unit = data.get("buy_unit")
    delivery = data.get("delivery")
    arenda_time = data.get("buy_arenda_time")
    del_quantity = 0
    quantity = 0
    if item_id in arenda_eq and delivery == 0:
        arenda_time = int(arenda_time)
        quantity = quant
        sum = price*quantity*arenda_time
    elif (item_id in arenda_items or item_id in arenda_eq) and delivery == 1:
        arenda_time = int(arenda_time)
        del_quantity = quant
        sum = del_price*del_quantity*arenda_time
    elif delivery == 1:
        del_quantity = quant
        sum = del_price * quant
        arenda_time = 0
    else:
        quantity = quant
        sum = price * quant
        arenda_time = 0
    city = data.get("city")
    comment = ''
    await commands.add_current_order(user_item, user_id, item_id, b_id, name, unit,
                                     price, del_price, quantity, del_quantity, arenda_time,
                                     sum, city, comment)
    await state.finish()
    await create_order(user_id)


def register_handlers_buy(dp: Dispatcher):
    dp.register_message_handler(cancel_buy, state="*", commands=['отмена'])
    dp.register_callback_query_handler(callback_buy, buy_item.filter())
    dp.register_message_handler(load_quantity, state=FSMClient.buy_quantity)
    dp.register_message_handler(indicate_arenda_time, state=FSMClient.buy_arenda_time)
    dp.register_message_handler(indicate_org, state=FSMClient.org_name)
    dp.register_message_handler(indicate_address, state=FSMClient.address)
    dp.register_message_handler(indicate_phone, content_types=ContentTypes.CONTACT, state=FSMClient.phone)

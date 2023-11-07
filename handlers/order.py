import pytz
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from create_bot import bot, operator, url_webhook, method, b24rest_request, method2
from handlers.states import get_order, FSMOrder, del_item, new_quantity
from handlers import quick_commands as commands
from keyboards import kb_client, order_kb, cancel_change_kb
from datetime import datetime

tz = pytz.timezone('Asia/Almaty')


async def create_order(user_id):
    client = await commands.select_client(user_id)
    cur_orders = await commands.select_current_orders(user_id)
    if cur_orders == [] or client == None:
        await bot.send_message(user_id, 'У Вас еще нет текущих заказов', reply_markup=kb_client)
    else:
        now = datetime.now(tz)
        date_time = now.strftime("%d.%m.%Y %H:%M")
        client_city = client.city
        org_name = client.org_name
        address = client.address
        phone = client.phone
        info_client = f'{date_time}\n<b>Заказ в корзине от {org_name}  из {client_city}:\n' \
            f'организация: {org_name}\nАдрес: {address}\nТелефон: {phone}\n</b>'
        asum = 0
        strpos = ""
        comment = ""
        for ret in cur_orders:
            if ret.del_quantity == 0:
                pos = f'{ret.name}\n в количестве {ret.quantity} {ret.unit}\n по цене {ret.price} тенге\n на сумму {ret.sum} тенге\nСклад:{ret.city}\n-------------------\n'
            elif ret.quantity == 0:
                pos = f'{ret.name}\n в количестве {ret.del_quantity} {ret.unit} с доставкой\n по цене {ret.del_price} тенге\n на сумму {ret.sum} тенге\nСклад:{ret.city}\n-------------------\n'
            else:
                pos = f'{ret.name}\n в количестве {ret.quantity} {ret.unit}\n по цене {ret.price} тенге\n' \
                      f'в количестве {ret.del_quantity} {ret.unit} с доставкой\n по цене {ret.del_price} тенге\n' \
                      f' на сумму {ret.sum} тенге\nСклад:{ret.city}\n-------------------\n'
            strpos = strpos + pos
            asum = asum + ret.sum
            comment = comment + ret.comment
        all_sum = f"Общая сумма Вашей покупки {asum} тенге\n"
        order = info_client + strpos + all_sum + f'Комментарий: {comment}'
        await bot.send_message(user_id, "Ваша заказ добавлен. Нажмите кнопку 'Отправить заказ'"
                             "чтобы его отправить, либо напишите дополнение", reply_markup=ReplyKeyboardRemove())

        await bot.send_message(user_id, order, parse_mode=types.ParseMode.HTML,
                             reply_markup=order_kb)


# @dp.message_handler(state="*", commands=['отменить'])
async def cancel_order(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    current_state = await state.get_state()
    if current_state is None:
        await message.answer('Ok', reply_markup=ReplyKeyboardRemove())
        await create_order(user_id)
        return
    await state.finish()
    await message.answer('Ok', reply_markup=ReplyKeyboardRemove())
    await create_order(user_id)


# @dp.callback_query_handler(text='order')
async def send_order(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    client = await commands.select_client(user_id)
    # client_id = client.user_id
    client_city = client.city
    client_org_name = client.org_name
    client_address = client.address
    client_phone = client.phone
    cur_order = await commands.select_current_orders(user_id)
    # status = 'Отправлен'
    order = call.message.text
    # order_text = order.replace('Заказ в корзине', 'Отправлен заказ')
    # await commands.add_order(user_id, order_text, status)
    # message_id = call.message.message_id
    #  mess = await bot.forward_message(operator, from_chat_id=call.from_user.id, message_id=message_id)
    parametr = {"fields": {
    "TITLE": client_org_name,
    "SOURCE_ID": 'UC_SLN7SG',
    "COMPANY_TITLE": client_org_name,
    "PHONE": [{'VALUE': client_phone, "VALUE_TYPE": "WORK"}],
    "ADDRESS": client_address,
    "ADDRESS_CITY": client_city,
    "COMMENTS": order}}
    response = b24rest_request(url_webhook, method, parametr)
    lead_id = str(response.get('result'))
    poses = []
    for ret in cur_order:
        if ret.del_quantity == 0:
            quantity = ret.quantity
        else:
            quantity = ret.del_quantity
        pos = {"PRODUCT_ID": ret.b_id,
                "PRICE": float(ret.price),
                "QUANTITY": quantity
                }
        poses.append(pos)
    parametr2 = {
        "id": lead_id,
        "rows": poses
    }
    response2 = b24rest_request(url_webhook, method2, parametr2)
    await bot.send_message(operator, order, reply_markup=InlineKeyboardMarkup().add(
    	InlineKeyboardButton('Взять в работу',
    						 callback_data=get_order.new(user_id=user_id, status='inwork'))))
    await commands.delete_cur_order(user_id)
    await call.message.answer('Ваш заказ отправлен', reply_markup=kb_client)
    await call.answer('Send')


# @dp.callback_query_handler(text='addorder')
async def order_add(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer("Выберите товары для того, чтобы добавить их в заказ", reply_markup=kb_client)
    await call.answer('Add')


# @dp.callback_query_handler(text='delitem')
async def delete_item_button(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    cur_orders = await commands.select_current_orders(user_id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    for ret in cur_orders:
        keyboard.insert(InlineKeyboardButton(ret.name,
                                             callback_data=del_item.new(item_id=ret.user_item)))
    keyboard.add(InlineKeyboardButton('Назад', callback_data='myorders'))
    await call.message.answer('Выберите товар, который вы хотите удалить',
                              reply_markup=keyboard)
    await call.answer('del')


# @dp.callback_query_handler(del_item.filter())
async def delete_item(call: types.CallbackQuery, callback_data: dict):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    user_item = callback_data.get("item_id")
    item = await commands.select_current_order(user_item)
    await item.delete()
    await call.message.answer(text=f'{item.name} удалена')
    await create_order(user_id)
    await call.answer(text=f'{item.name} удалена', show_alert=True)


# @dp.callback_query_handler(text='change')
async def change_quantity(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    cur_orders = await commands.select_current_orders(user_id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    for ret in cur_orders:
        if ret.del_quantity == 0:
            keyboard.insert(InlineKeyboardButton(ret.name,
                                             callback_data=new_quantity.new(user_item=ret.user_item, delivery=0)))
        elif ret.quantity == 0:
            keyboard.insert(InlineKeyboardButton(ret.name,
                                                 callback_data=new_quantity.new(user_item=ret.user_item, delivery=1)))
        else:
            keyboard.insert(InlineKeyboardButton(ret.name,
                                                 callback_data=new_quantity.new(user_item=ret.user_item, delivery=2)))
    keyboard.add(InlineKeyboardButton('Назад', callback_data='myorders'))
    await call.message.answer('Выберите товар количество которого вы хотите изменить ',
                              reply_markup=keyboard)
    await call.answer('change')


# @dp.callback_query_handler(new_quantity.filter())
async def callback_new_quantity(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    user_item = callback_data.get("user_item")
    delivery = callback_data.get("delivery")
    item = await commands.select_current_order(user_item)
    if int(delivery) == 0:
        await state.update_data(order_delivery=0)
        await state.update_data(order_price=item.price)
        await call.answer(text=f'Укажите новое количество {item.name}.', show_alert=True)
        await bot.send_message(user_id, text=f"Укажите новое количество {item.name}",
                               reply_markup=cancel_change_kb)
        await FSMOrder.new_quantity.set()
        await state.update_data(order_item_id=user_item)
    elif int(delivery) == 1:
        await state.update_data(order_delivery=1)
        await state.update_data(order_price=item.del_price)
        await call.answer(text=f'Укажите новое количество {item.name}.', show_alert=True)
        await bot.send_message(user_id, text=f"Укажите новое количество {item.name}",
                               reply_markup=cancel_change_kb)
        await FSMOrder.new_quantity.set()
        await state.update_data(order_item_id=user_item)
    else:
        await call.message.answer(f'В вашем заказе есть {item.name} c доставкой и без доставки',
                                  reply_markup=InlineKeyboardMarkup(row_width=2, inline_keyboard=[
                                      [InlineKeyboardButton(item.name,
                                                            callback_data=new_quantity.new(user_item=item.user_item, delivery=0)),
                                       InlineKeyboardButton(f'{item.name} с доставкой',
                                                            callback_data=new_quantity.new(user_item=item.user_item, delivery=1))],
                                      [InlineKeyboardButton('Назад', callback_data='myorders')]
                                  ]))
        await call.answer("Choose")


# @dp.message_handler(state=FSMOrder.new_quantity)
async def load_new_quantity(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        answer = int(message.text)
    except ValueError:
        await message.answer("Укажите количество в цифрах")
        return
    answer = message.text
    await state.update_data(new_quantity=answer)
    data = await state.get_data()
    new_quantity = int(data.get('new_quantity'))
    user_item = data.get('order_item_id')
    delivery = data.get("order_delivery")
    price = int(data.get('order_price'))
    new_sum = new_quantity*price
    await commands.change_quantity_cur_order(user_item, new_quantity, new_sum, delivery)
    await message.answer('Количество товара успешно изменено', reply_markup=ReplyKeyboardRemove())
    await state.finish()
    await create_order(user_id)


# @dp.callback_query_handler(text='comment')
async def comment_user(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer('Напишите комментарий')
    await FSMOrder.comment.set()
    await call.answer('comment')


# @dp.message_handler(state=FSMOrder.comment)
async def set_comment(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    comment = message.text
    await commands.set_comment(user_id, comment)
    await create_order(user_id)
    await state.reset_state()


# @dp.callback_query_handler(text='delall')
async def delete_all_items(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    await commands.delete_cur_order(user_id)
    await call.message.answer(text='Заказ удален. У вас нет заказов. Выберите товары и создайте заказ',
                              reply_markup=kb_client)
    await call.answer(text='Ваша корзина пуста')


# @dp.callback_query_handler(text='myorders')
async def client_orders(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    await create_order(user_id)


# @dp.callback_query_handler(text='ordershistory')
async def get_history_orders(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    try:
        orders = await commands.select_order(user_id)
        await call.message.answer(orders.order_text, parse_mode=types.ParseMode.HTML, reply_markup=kb_client)
    except:
        await call.message.answer("Вы еще ничего не заказывали", reply_markup=kb_client)
    await call.answer('История заказов')



def register_handlers_order(dp: Dispatcher):
    dp.register_message_handler(cancel_order, state="*", commands=["отменить"])
    dp.register_callback_query_handler(send_order, text="order")
    dp.register_callback_query_handler(order_add, text="addorder")
    dp.register_callback_query_handler(delete_item_button, text="delitem")
    dp.register_callback_query_handler(delete_item, del_item.filter())
    dp.register_callback_query_handler(change_quantity, text="change")
    dp.register_callback_query_handler(callback_new_quantity, new_quantity.filter())
    dp.register_message_handler(load_new_quantity, state=FSMOrder.new_quantity)
    dp.register_callback_query_handler(comment_user, text="comment")
    dp.register_message_handler(set_comment, state=FSMOrder.comment)
    dp.register_callback_query_handler(delete_all_items, text="delall")
    dp.register_callback_query_handler(client_orders, text="myorders")
    dp.register_callback_query_handler(get_history_orders, text="ordershistory")

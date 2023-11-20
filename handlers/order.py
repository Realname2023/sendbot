import pytz
import re
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from create_bot import bot, operator, url_webhook, method, b24rest_request, method2, arenda_items, arenda_eq
from handlers.states import client_order, FSMOrder, del_item, new_quantity
from handlers import quick_commands as commands
from keyboards import kb_client, order_kb, cancel_change_kb
from datetime import datetime

tz = pytz.timezone('Asia/Almaty')


async def create_order(user_id):
    client = await commands.select_client(user_id)
    cur_orders = await commands.select_current_orders(user_id)
    if cur_orders == [] or client == None:
        await bot.send_message(user_id, 'У Вас еще нет текущих заказов. Выберите товары и создайте заказ', reply_markup=kb_client)
    else:
        now = datetime.now(tz)
        date_time = now.strftime("%d.%m.%Y %H:%M")
        client_city = client.city
        org_name = client.org_name
        address = client.address
        phone = client.phone
        info_client = f'{date_time}\n<b>Заказ от {org_name}  из {client_city}:\n' \
            f'организация: {org_name}\nАдрес: {address}\nТелефон: {phone}\n</b>'
        asum = 0
        strpos = ""
        comment = ""
        for ret in cur_orders:
            if ret.arenda_time != 0 and ret.del_quantity == 0:
                pos = f"{ret.name} по договору\nв количестве {ret.quantity} {ret.unit} на {ret.arenda_time} мес.\n по цене {ret.price} тенге\n на сумму {ret.sum} тенге\nСклад:{ret.city}\n-------------------\n"
            elif ret.arenda_time != 0 and ret.quantity == 0:
                pos = f"{ret.name}\n в количестве {ret.del_quantity} {ret.unit} на {ret.arenda_time} мес.\n по цене {ret.del_price} тенге\n на сумму {ret.sum} тенге\nСклад:{ret.city}\n-------------------\n"
            elif ret.del_quantity == 0:
                pos = f"{ret.name}\n в количестве {ret.quantity} {ret.unit}\n по цене {ret.price} тенге\n на сумму {ret.sum} тенге\nСклад:{ret.city}\n-------------------\n"
            elif ret.quantity == 0:
                pos = f"{ret.name}\n в количестве {ret.del_quantity} {ret.unit} с доставкой\n по цене {ret.del_price} тенге\n на сумму {ret.sum} тенге\nСклад:{ret.city}\n-------------------\n"
            else:
                pos = (
                    f"{ret.name}\n в количестве {ret.quantity} {ret.unit}\n по цене {ret.price} тенге\n"
                    f"в количестве {ret.del_quantity} {ret.unit} с доставкой\n по цене {ret.del_price} тенге\n"
                    f" на сумму {ret.sum} тенге\nСклад:{ret.city}\n-------------------\n"
                )
            strpos = strpos + pos
            asum = asum + ret.sum
            comment = comment + ret.comment
        all_sum = f"Общая сумма Вашей покупки {asum} тенге\n"
        order = info_client + strpos + all_sum + f'Комментарий: {comment}'
        await bot.send_message(user_id,
                               "Ваша заказ добавлен. Нажмите кнопку 'Отправить заказ'"
                               "чтобы заказать товары, либо дополните заказ, используя остальные кнопки"
                               ,
                               reply_markup=ReplyKeyboardRemove())

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
    id_bot = str(user_id)
    client = await commands.select_client(user_id)
    # client_id = client.user_id
    client_city = client.city
    client_org_name = client.org_name
    client_address = client.address
    client_phone = client.phone
    tittle = client.full_name
    linc = "не указан"
    user_name = client.user_name
    if user_name is not None:
        linc = f"https://t.me/{user_name}"
    cur_order = await commands.select_current_orders(user_id)
    order = call.message.text
    parametr = {"fields": {
    "TITLE": tittle,
    "SOURCE_ID": 'UC_SLN7SG',
    "COMPANY_TITLE": client_org_name,
    "PHONE": [{'VALUE': client_phone, "VALUE_TYPE": "WORK"}],
    "ADDRESS": client_address,
    "ADDRESS_2": linc,
    "ADDRESS_CITY": client_city,
    "IM": [{	
        "VALUE_TYPE": "Telegram",
        "VALUE": f"imol|telegrambot|5|{id_bot}|4153"}],
    "COMMENTS": order}}
    response = await b24rest_request(url_webhook, method, parametr)
    lead_id = str(response.get('result'))
    poses = []
    for ret in cur_order:
        if ret.del_quantity == 0:
            quantity = ret.quantity
            price = ret.price
        else:
            quantity = ret.del_quantity
            price = ret.del_price
        if ret.item_id in arenda_eq or ret.item_id in arenda_items:
            for i in range(quantity):
                i = {"PRODUCT_ID": ret.b_id,
                        "PRICE": float(price),
                        "QUANTITY": ret.arenda_time,
                        "MEASURE_CODE": 323
                        }
                poses.append(i)
        else:
            pos = {"PRODUCT_ID": ret.b_id,
                "PRICE": float(price),
                "QUANTITY": quantity
                }
            poses.append(pos)
    parametr2 = {
        "id": lead_id,
        "rows": poses
    }
    await b24rest_request(url_webhook, method2, parametr2)
    await bot.send_message(
        operator, order, reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("Уточнить данные заказчика", callback_data=client_order.new(
                    user_id=user_id))))
    await call.message.answer("Ваш заказ отправлен. Пожалуйста, нажмите кнопку 'Написать оператору подтвердить'"
                              "для подтверждения заказа и напишите какое-нибудь сообщение",
                              reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("Написать оператору подтвердить", url='https://t.me/VTGonlinebot')))
    await call.message.answer("==================================", reply_markup=kb_client)
    await commands.delete_cur_order(user_id)
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
        keyboard.insert(
            InlineKeyboardButton(
                ret.name,
                callback_data=new_quantity.new(user_item=ret.user_item, 
                                                quantity=ret.quantity,
                                                del_quantity=ret.del_quantity)
            )
        )
    keyboard.add(InlineKeyboardButton("Назад", callback_data="myorders"))
    await call.message.answer(
        "Выберите товар количество или время аренды, которого вы хотите изменить ", reply_markup=keyboard
    )
    await call.answer("change")


# @dp.callback_query_handler(new_quantity.filter())
async def callback_new_quantity(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    user_item = callback_data.get("user_item")
    quantity = callback_data.get("quantity")
    del_quantity = callback_data.get("del_quantity")
    item = await commands.select_current_order(user_item)
    if int(del_quantity) != 0 and int(quantity) != 0:
        await call.message.answer(
            f"В вашем заказе есть {item.name} c доставкой и без доставки",
            reply_markup=InlineKeyboardMarkup(
                row_width=2,
                inline_keyboard=[
                    [InlineKeyboardButton(
                            item.name,
                            callback_data=new_quantity.new(
                                user_item=item.user_item,
                                quantity=quantity,
                                del_quantity=0
                            ),
                        ),
                        InlineKeyboardButton(
                            f"{item.name} с доставкой",
                            callback_data=new_quantity.new(
                                user_item=item.user_item,
                                quantity=0,
                                del_quantity=del_quantity
                            ),
                        ),
                    ],
                    [InlineKeyboardButton("Назад", callback_data="myorders")],
                ],
            )
        )
        await call.answer("Choose")
    else:
        await call.answer(
            text=f"Укажите новое количество {item.name}.", show_alert=True
        )
        await bot.send_message(
            user_id,
            text=f"Укажите новое количество {item.name}",
            reply_markup=cancel_change_kb,
        )
        await FSMOrder.new_quantity.set()
        await state.update_data(order_user_item=user_item)
        await state.update_data(order_item_id=item.item_id)
        if int(del_quantity) == 0:
            await state.update_data(order_delivery=0)
        
        else:
            await state.update_data(order_delivery=1)


# @dp.message_handler(state=FSMOrder.new_quantity)
async def load_new_quantity(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    pat = r"[^0-9]"
    answer = re.sub(pat, "", message.text)
    try:
        answer = int(message.text)
    except ValueError:
        await message.answer("Укажите количество в цифрах")
        return
    answer = message.text
    await state.update_data(new_quantity=answer)
    data = await state.get_data()
    new_quantity = int(data.get("new_quantity"))
    user_item = data.get("order_user_item")
    item_id = data.get("order_item_id")
    delivery = data.get("order_delivery")
    await commands.change_quantity_cur_order(user_item, new_quantity, delivery)
    await message.answer(
        "Количество товара успешно изменено", reply_markup=ReplyKeyboardRemove()
    )
    if item_id in arenda_eq or item_id in arenda_items:
        await message.answer("Укажите новое время аренды", reply_markup=cancel_change_kb)
        await FSMOrder.new_arenda_time.set()
    else:
        await state.finish()
        await create_order(user_id)


# @dp.message_handler(state=FSMOrder.new_arenda_time)
async def load_new_arenda_time(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    pat = r"[^0-9]"
    answer = re.sub(pat, "", message.text)
    try:
        answer = int(message.text)
    except ValueError:
        await message.answer("Укажите время аренды в цифрах")
        return
    answer = message.text
    data = await state.get_data()
    user_item = data.get("order_user_item")
    new_time_arenda = int(answer)
    await commands.change_arenda_time(user_item, new_time_arenda)
    await state.finish()
    await create_order(user_id)


# @dp.callback_query_handler(text='comment')
async def comment_user(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer('Напишите Ваш комментарий к заказу', reply_markup=cancel_change_kb)
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


def register_handlers_order(dp: Dispatcher):
    dp.register_message_handler(cancel_order, state="*", commands=["отменить"])
    dp.register_callback_query_handler(send_order, text="order")
    dp.register_callback_query_handler(order_add, text="addorder")
    dp.register_callback_query_handler(delete_item_button, text="delitem")
    dp.register_callback_query_handler(delete_item, del_item.filter())
    dp.register_callback_query_handler(change_quantity, text="change")
    dp.register_callback_query_handler(callback_new_quantity, new_quantity.filter())
    dp.register_message_handler(load_new_quantity, state=FSMOrder.new_quantity)
    dp.register_message_handler(load_new_arenda_time, state=FSMOrder.new_arenda_time)
    dp.register_callback_query_handler(comment_user, text="comment")
    dp.register_message_handler(set_comment, state=FSMOrder.comment)
    dp.register_callback_query_handler(delete_all_items, text="delall")
    dp.register_callback_query_handler(client_orders, text="myorders")

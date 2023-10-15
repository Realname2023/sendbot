from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ChatType
from create_bot import bot, dp, operator
from handlers.states import select_city, get_order, FSMClient, FSMOrder, del_item, new_quantity
from handlers import quick_commands as commands
from keyboards import kb_client, buying_kb, cancel_buy_kb, order_kb
from data_base.base_db import Client
import time


async def create_order(user_id, message: types.Message, s=0):
    client = await commands.select_client(user_id)
    cur_orders = await commands.select_current_orders(user_id)
    if cur_orders == [] or client == None:
        await message.answer('У Вас еще нет текущих заказов', reply_markup=kb_client)
    else:
        struct = time.localtime(time.time())
        seconds = time.strftime('%d.%m.%Y %H:%M', struct)
        client_city = client.city
        org_name = client.org_name
        address = client.address
        phone = client.phone
        info_client = f'{seconds}\n<b>Заказ в корзине от {org_name}  из {client_city}:\n' \
            f'организация: {org_name}\nАдрес: {address}\nТелефон: {phone}\n</b>'
        asum = 0
        strpos = ""
        comment = ""
        for ret in cur_orders:
            pos = f'{ret.name}\n в количестве {ret.quantity} {ret.unit}\n по цене {ret.price} тенге\n на сумму {ret.sum} тенге\nСклад:{ret.city}\n-------------------\n'
            strpos = strpos + pos
            asum = asum + ret.sum
            comment = comment + ret.comment
        all_sum = f"Общая сумма Вашей покупки {asum} тенге\n"
        order = info_client + strpos + all_sum + f'Комментарий: {comment}'
        await message.answer("Ваша заказ добавлен. Нажмите кнопку 'Отправить заказ'"
                             "чтобы его отправить, либо напишите дополнение", reply_markup=ReplyKeyboardRemove())
        if s == 0:
            await message.answer(order, parse_mode=types.ParseMode.HTML,
                             reply_markup=order_kb)
        else:
            await message.answer('Ваш заказ отправлен', reply_markup=kb_client)
        return order




@dp.callback_query_handler(text='order')
async def order(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    message = call.message
    order = await create_order(user_id, message, 1)
    status = 'Отправлен'
    order_text = order.replace('Заказ в корзине', 'Отправлен заказ')
    await commands.add_order(user_id, order_text, status)
    message_id = call.message.message_id
    mess = await bot.forward_message(operator, from_chat_id=call.from_user.id, message_id=message_id)
    await bot.send_message(operator, '^^^^^^^^^^^^^^^^^^^^^^^^^^^', reply_markup=InlineKeyboardMarkup().add(
    	InlineKeyboardButton('Взять в работу',
    						 callback_data=get_order.new(user_id=user_id, status='inwork',
    													 message_id=mess.message_id))))
    await commands.delete_cur_order(user_id)
    await call.answer('Send')


@dp.callback_query_handler(text='addorder')
async def order(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer("Выберите товары для того, чтобы добавить их в заказ", reply_markup=kb_client)
    await call.answer('Add')


@dp.callback_query_handler(text='comment')
async def set_comment(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer('Напишите комментарий')
    await FSMOrder.comment.set()
    await call.answer('comment')


@dp.message_handler(state=FSMOrder.comment)
async def set_comment(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    comment = message.text
    await commands.set_comment(user_id, comment)
    await create_order(user_id, message)
    await state.reset_state()


@dp.callback_query_handler(text='delitem')
async def delete_item(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    cur_orders = await commands.select_current_orders(user_id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    for ret in cur_orders:
        keyboard.insert(InlineKeyboardButton(ret.name,
                                             callback_data=del_item.new(item_id=ret.item_id)))
    keyboard.add(InlineKeyboardButton('Назад', callback_data='myorders'))
    await call.message.answer('Выберите товар, который вы хотите удалить',
                              reply_markup=keyboard)
    await call.answer('del')


@dp.callback_query_handler(del_item.filter())
async def delete_item(call: types.CallbackQuery, callback_data: dict):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    message = call.message
    item_id = callback_data.get("item_id")
    item = await commands.select_current_order(user_id, item_id)
    await commands.delete_item_cur_order(user_id, item_id)
    await call.message.answer(text=f'{item.name} удалена')
    await create_order(user_id, message)
    await call.answer(text=f'{item.name} удалена', show_alert=True)


@dp.callback_query_handler(text='change')
async def change_quantity(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    cur_orders = await commands.select_current_orders(user_id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    for ret in cur_orders:
        keyboard.insert(InlineKeyboardButton(ret.name,
                                             callback_data=new_quantity.new(item_id=ret.item_id, price=ret.price)))
    keyboard.add(InlineKeyboardButton('Назад', callback_data='myorders'))
    await call.message.answer('Выберите товар количество которого вы хотите изменить ',
                              reply_markup=keyboard)
    await call.answer('change')


@dp.callback_query_handler(new_quantity.filter())
async def callback_new_quantity(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    item_id = callback_data.get("item_id")
    item = await commands.select_current_order(user_id, item_id)
    price = callback_data.get("price")
    await call.answer(text=f'Укажите новое количество {item.name}.', show_alert=True)
    await bot.send_message(user_id, text=f"Укажите новое количество {item.name}")
    await FSMOrder.new_quantity.set()
    await state.update_data(order_item_id=item_id)
    await state.update_data(order_price=price)


@dp.message_handler(state=FSMOrder.new_quantity)
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
    item_id = data.get('order_item_id')
    price = int(data.get('order_price'))
    new_sum = new_quantity*price
    await commands.change_quantity_cur_order(user_id, item_id, new_quantity, new_sum)
    await message.answer(f'Количество товара успешно изменено')
    await state.finish()
    await create_order(user_id, message)




@dp.callback_query_handler(text='delall')
async def delete_all_items(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    await commands.delete_cur_order(user_id)
    await call.message.answer(text='Заказ удален. У вас нет заказов. Выберите товары и создайте заказ',
                              reply_markup=kb_client)
    await call.answer(text='Ваша корзина пуста')


@dp.callback_query_handler(text='myorders')
async def client_orders(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    message = call.message
    await create_order(user_id, message)


@dp.callback_query_handler(text='ordershistory')
async def get_history_orders(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    try:
        orders = await commands.select_order(user_id)
        await call.message.answer(orders.order_text, parse_mode=types.ParseMode.HTML, reply_markup=kb_client)
    except:
        await call.message.answer("Вы еще ничего не заказывали", reply_markup=kb_client)
    await call.answer('История заказов')
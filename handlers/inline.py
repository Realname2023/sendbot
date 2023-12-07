from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import bot, arenda_items, arenda_eq
from handlers import quick_commands as commands
from handlers.states import select_cat, buy_item
from keyboards.client_kb import kb_client


# @dp.callback_query_handler(select_cat.filter())
async def select_category(call: types.CallbackQuery, callback_data: dict):
    call_data = callback_data.get("cat")
    if call_data.startswith('buy_'):
        call_data = call_data.replace('buy_', '')
        await call.message.edit_reply_markup()
        try:
            ret = await commands.select_item(call_data)
            await bot.send_message(call.from_user.id,
                                   text='Наше предложение')
            if ret.item_id in arenda_items:
                await bot.send_photo(call.from_user.id, ret.photo,
                                     f'<b>{ret.name}</b>\n{ret.description}\nСклад: {ret.city} '
                                     f'\nАренда: {ret.del_price} тенге за {ret.unit}'
                                     f' в месяц с залогом по стоимости баллона (40000 тенге)',
                                     parse_mode=types.ParseMode.HTML,
                                     reply_markup=InlineKeyboardMarkup(row_width=1, inline_keyboard=[
                                         [InlineKeyboardButton('Аренда',
                                                               callback_data=buy_item.new(item_id=ret.item_id,
                                                                                          price=ret.del_price))],
                                         [InlineKeyboardButton('Назад', callback_data=select_cat.new(ret.city_back))]
                                     ]))
            elif ret.item_id in arenda_eq:
                await bot.send_photo(call.from_user.id, ret.photo,
                                     f'<b>{ret.name}</b>\n{ret.description}\nСклад: {ret.city}\n'
                                     f'Аренда к договору поставки газов: {ret.price} тенге за {ret.unit} в месяц\n'
                                     f'Аренда без договора {ret.del_price} тенге за {ret.unit} в месяц',
                                     parse_mode=types.ParseMode.HTML,
                                     reply_markup=InlineKeyboardMarkup(row_width=1, inline_keyboard=[
                                         [InlineKeyboardButton('Аренда к договору',
                                                               callback_data=buy_item.new(item_id=ret.item_id,
                                                                                          price=ret.price))],
                                         [InlineKeyboardButton('Аренда без договора',
                                                               callback_data=buy_item.new(item_id=ret.item_id,
                                                                                          price=ret.del_price))],
                                         [InlineKeyboardButton('Назад', callback_data=select_cat.new(ret.city_back))]
                                     ]))
            elif ret.del_price == 0:
                await bot.send_photo(call.from_user.id, ret.photo,
                                     f'<b>{ret.name}</b>\n{ret.description}\nСклад: {ret.city} '
                                     f'\nЦена {ret.price} тенге за {ret.unit}',
                                     parse_mode=types.ParseMode.HTML,
                                     reply_markup=InlineKeyboardMarkup(row_width=1, inline_keyboard=[
                                        [InlineKeyboardButton('Купить',callback_data=buy_item.new(item_id=ret.item_id,
                                                                                                  price=ret.price))],
                                         [InlineKeyboardButton('Назад', callback_data=select_cat.new(ret.city_back))]
                                     ]))
            else:
                await bot.send_photo(call.from_user.id, ret.photo,
                                     f'<b>{ret.name}</b>\n{ret.description}\nСклад: {ret.city} '
                                     f'\nЦена: {ret.price} тенге за {ret.unit}\nЦена с доставкой: {ret.del_price} тенге',
                                     parse_mode=types.ParseMode.HTML,
                                     reply_markup=InlineKeyboardMarkup(row_width=1, inline_keyboard=[
                                         [InlineKeyboardButton('Купить',
                                                               callback_data=buy_item.new(item_id=ret.item_id,
                                                                                          price=ret.price))],
                                         [InlineKeyboardButton('Купить с доставкой',
                                                               callback_data=buy_item.new(item_id=ret.item_id,
                                                                                          price=ret.del_price))],
                                         [InlineKeyboardButton('Назад', callback_data=select_cat.new(ret.city_back))]
                                     ]))
        except:
            await bot.send_message(call.from_user.id, text='Товар не найден. Нажмите кнопку "Написать оператору", для получения информации по товару',
                                   reply_markup=kb_client)
    else:
        await call.message.edit_reply_markup()
        read = await commands.select_category(call_data)
        row_width = read[0].row_width
        text = read[0].edit_text
        keyboard = InlineKeyboardMarkup(row_width=row_width)
        for ret in read:
            if ret.button_data == "myorders" or ret.button_data == 'back':
                keyboard.add(
                    InlineKeyboardButton(ret.button_text, callback_data=ret.button_data))
            elif call_data == ret.button_data:
                keyboard.add(InlineKeyboardButton(ret.button_text, callback_data=select_cat.new(cat=call_data)))
            else:
                keyboard.insert(
                    InlineKeyboardButton(ret.button_text, callback_data=select_cat.new(cat=ret.button_data)))
        await call.message.answer(text, reply_markup=keyboard)
    await call.answer('Выберите')

# @dp.callback_query_handler(text='back')
async def back_main(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer('Главное меню. Выберите товары и создайте заказ', reply_markup=kb_client)
    await call.answer('Главное меню')


def register_handlers_inline(dp: Dispatcher):
    dp.register_callback_query_handler(select_category, select_cat.filter())
    dp.register_callback_query_handler(back_main, text='back')

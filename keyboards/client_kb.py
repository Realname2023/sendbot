from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from handlers.states import select_cat


kb_client = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [InlineKeyboardButton(text='Газы', callback_data=select_cat.new(cat='cities')),
    InlineKeyboardButton('Баллоны для газов',
                          callback_data=select_cat.new(cat='country'))],
    [InlineKeyboardButton('Криогенные жидкости', callback_data='liquid'),
    InlineKeyboardButton('Оборудование',
                          callback_data=select_cat.new('eq_cat'))],
    [InlineKeyboardButton('Запчасти и услуги', callback_data=select_cat.new('complects'))],
    [InlineKeyboardButton(text='Моя корзина', callback_data='myorders'),
    InlineKeyboardButton(text='Акции', callback_data='actions')],
    [InlineKeyboardButton(text='Адреса контакты', callback_data='adres'),
    InlineKeyboardButton(text='График работы', callback_data='time')],
    [InlineKeyboardButton('Отзывы полезные ссылки', callback_data='voices')],
    [InlineKeyboardButton('Написать оператору', url='https://t.me/VTGonlinebot')]
])

clb = KeyboardButton('/отмена')
cancel_buy_kb = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_buy_kb.add(clb)

clo = KeyboardButton('/отменить')
cancel_change_kb = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_change_kb.add(clo)

order_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [InlineKeyboardButton(text='Отправить заказ', callback_data='order')],
    [InlineKeyboardButton(text='Добавить товар в заказ', callback_data='addorder')],
    [InlineKeyboardButton(text='Удалить товар из заказа', callback_data='delitem')],
    [InlineKeyboardButton(text=f'Изменить количество товаров\nили аренду', callback_data='change')],
    [InlineKeyboardButton(text='Добавить комментарий к заказу', callback_data='comment')],
    [InlineKeyboardButton(text='Удалить заказ', callback_data='delall')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]
])

buying_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [InlineKeyboardButton('Назад', callback_data='back')]])


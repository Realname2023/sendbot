from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

oper_panel = ReplyKeyboardMarkup(resize_keyboard=True)

op1 = KeyboardButton('/Закрыть_чат')
op2 = KeyboardButton('/Входящие_заказы')
op3 = KeyboardButton('/Входящие_сообщения')

oper_panel.add(op1).add(op2).add(op3)
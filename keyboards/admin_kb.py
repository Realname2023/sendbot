from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_load = KeyboardButton('/Загрузить')
button_load_cat = KeyboardButton('/Загрузить_категорию')
button_delete = KeyboardButton('/Загрузка_из_файла')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load).add(button_load_cat).add(button_delete)
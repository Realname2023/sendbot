from aiogram import types, Dispatcher
from aiogram.types import InputFile
from create_bot import bot, operator
from handlers.throttling import rate_limit
from keyboards import kb_client, operator_kb
from handlers import quick_commands as commands


# @dp.message_handler(commands=['start', 'help'])
@rate_limit(limit=2)
async def command_start(message: types.Message):
    photo = InputFile('media/VTG.png')
    chat_id = message.chat.id
    if message.from_user.id == operator:
        await bot.send_photo(chat_id=chat_id, photo=photo)
        await message.answer('Привет оператор', reply_markup=operator_kb.oper_panel)
    else:
        try:
            read = await commands.select_user(message.from_user.id)
            user = read.user_id
            await bot.send_photo(chat_id=chat_id, photo=photo, caption='Здравствуйте. Вы написали в компанию ТОО "ВостокТехГаз".Вы можете оставить вашу заявку  и мы обработаем ее в течение часа.',
                                 reply_markup=kb_client)

        except Exception:
            await commands.add_user(user_id=message.from_user.id,
									first_name=message.from_user.first_name,
									last_name=message.from_user.last_name,
									user_name=message.from_user.username,
									status='active'
									)
            await bot.send_photo(chat_id=chat_id, photo=photo,
                                 caption='Здравствуйте. Вы написали в компанию ТОО "ВостокТехГаз".Вы можете оставить вашу заявку  и мы обработаем ее в течение часа.',
                                 reply_markup=kb_client)


# @dp.callback_query_handler(text='adres')
async def show_place(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer('Адреса:\nг. Семей, ул. Джангильдина 82/1,\n'
                              'г. Усть-Каменогорск, уд. Абая 181,\n'
                              'г. Павлодар, ул. Малая объездная 9/1,\n'
                              'г. Астана, проспект Абая 99/1\n'
                              'Контакты:\n'
                              'Единый номер: +77059565000 WhatsApp',
                                        reply_markup=kb_client)
    await call.answer('адреса')

# @dp.callback_query_handler(text='time')
async def show_work_time(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer(
        'Семей 08.30 - 17.00,\nУсть-Каменогорск 08.00 - 17.00.\nПавлодар 08.30 - 17.30,\nАстана 08.30 - 17.00',
        reply_markup=kb_client)
    await call.answer('график работы')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start", "help"])
    dp.register_callback_query_handler(show_place, text="adres")
    dp.register_callback_query_handler(show_work_time, text="time")
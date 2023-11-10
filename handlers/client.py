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
    await call.message.answer("Адреса:\nг. г. Семей, ул. Джангильдина 82/1, район областной больницы\n"
        "https://go.2gis.com/us0av\n"
        "\n"
        "г. Усть-Каменогорск, ул. Абая 181, возле рынка 'Дина'\n"
        "https://go.2gis.com/o9b30v\n"
        "\n"
        "г. Павлодар, ул. Малая объездная 9/1, за ТЦ 'Батырмолл'\n"
        "https://go.2gis.com/hdsq0\n"
        "\n"
        "г. Астана, проспект Абая 99/1, бывшая база ВторЧерМет\n"
        "https://go.2gis.com/xhrt6\n"
        "\n"
        "Контакты:\n"
        "Единый номер: +77059565000 WhatsApp\n",
                                        reply_markup=kb_client)
    await call.answer('адреса')

# @dp.callback_query_handler(text='time')
async def show_work_time(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer(
        'Семей 08.30 - 17.00,\nУсть-Каменогорск 08.00 - 17.00.\nПавлодар 08.30 - 17.30,\nАстана 08.30 - 17.00',
        reply_markup=kb_client)
    await call.answer('график работы')


# @dp.callback_query_handler(text="actions")
async def actions(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    user = call.from_user.id
    action = await commands.select_action()
    if action != None:
        await bot.send_photo(user, action.photo, caption=action.text,
                             reply_markup=kb_client)
    else:
        await call.message.answer("Пока никаких акций нету",
                                  reply_markup=kb_client)
    await call.answer("акции")


# @dp.callback_query_handler(text="voices")
async def voices(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer("Полезные ссылки:\n"
                              "https://wa.me/message/6KT7KF6BOGEJA1\n"
                              "\n"
                              "https://www.instagram.com/vtg_gaz/\n"
                              "\n"
                              "vostoktehgaz@mail.ru\n"
                              "\n"
                              "Отзывы можно оставить по ссылкам:\n"
                              "\n"
                              "https://go.2gis.com/us0av\n"
                              "\n"
                              "https://go.2gis.com/o9b30v\n"
                              "\n"
                              "https://go.2gis.com/o9b30v\n"
                              "\n"
                              "https://go.2gis.com/xhrt6",
                              reply_markup=kb_client)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start", "help"])
    dp.register_callback_query_handler(show_place, text="adres")
    dp.register_callback_query_handler(show_work_time, text="time")
    dp.register_callback_query_handler(actions, text="actions")
    dp.register_callback_query_handler(voices, text="voices")

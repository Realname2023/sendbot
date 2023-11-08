from aiogram import types
from create_bot import dp, bot, operator, admin, sender_photo
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ContentTypes, ContentType
from handlers import quick_commands as commands
from handlers.states import client_order, get_order, get_delivery

all_commands = ['/отмена', '/start', '/stop', '/Закрыть_чат', '/Входящие_заказы', '/Входящие_сообщения', '/Загрузить', '/Загрузить_категорию',
'/Загрузка_из_файла', '/moderator', '/moderator2', '/moderator3']


# @dp.callback_query_handler(client_order.filter())
# async def accept_order(call: types.CallbackQuery, callback_data: dict):
#     await call.message.edit_reply_markup()
#     user = int(callback_data.get("user_id"))
#     # await commands.add_active_user(user)
#     await bot.send_message(user, text='Здлавствуйте с Вами скоро свяжуться')
#     await call.answer(text='Ответ на заявку отправлен', show_alert=True)


@dp.message_handler(lambda message: message.from_user.id not in [operator, admin, sender_photo] and message.text not in all_commands,
                    content_types=ContentTypes.ANY)
async def other_message(message: types.Message):
    await message.delete()
    # sender_id = message.from_user.id
    # # print(sender_id, message.chat.id, message.from_user.full_name)
    # name = message.from_user.full_name
    # if message.photo:
    #     await bot.send_photo(operator, photo=message.photo[-1].file_id)
    #     await bot.send_photo(sender_id, photo=message.photo[-1].file_id,
    #                          caption=message.photo[-1].file_id)
    #     # await message.answer(message.photo[-1].file_id)
    # elif message.voice:
    #     await bot.send_voice(operator, voice=message.voice.file_id,
    #                          caption=f'{name}')
    # elif message.audio:
    #     await bot.send_audio(operator, audio=message.audio.file_id,
    #                          caption=f'{name}')
    # elif message.document:
    #     await bot.send_document(operator, document=message.document.file_id,
    #                             caption=f'{name}')
    # elif message.video:
    #     await bot.send_video(operator, video=message.video.file_id,
    #                          caption=f'{name}')
    # elif message.contact:
    #     await bot.send_contact(operator, message.contact.phone_number, message.contact.first_name)
    # elif message.sticker:
    #     await bot.send_sticker(operator, sticker=message.sticker.file_id)
    # else:
    #     await bot.send_message(operator,
    #                            text=f"Пользователь {name} написал: {message.text}")
    #     # print(message.chat.id)
    # else:
    #     user_id = sender_id + 1
    #     await commands.add_message_user(user_id, name)
    #     if message.photo:
    #         await messages_db.inbox_messages(user_id, message.photo[-1].file_id)
    #     elif message.voice:
    #         await messages_db.inbox_messages(user_id, message.voice.file_id)
    #     elif message.audio:
    #         await messages_db.inbox_messages(user_id, message.audio.file_id)
    #     elif message.document:
    #         await messages_db.inbox_messages(user_id, message.document.file_id)
    #     elif message.video:
    #         await messages_db.inbox_messages(user_id, message.video.file_id)
    #     elif message.sticker:
    #         await messages_db.inbox_messages(user_id, message.sticker.file_id)
    #     else:
    #         await messages_db.inbox_messages(user_id, message.text)
    #     await message.answer('Оператор скоро с Вами свяжиться')
@dp.message_handler(lambda message: message.from_user.id == sender_photo and message.text not in all_commands,
                    content_types=ContentTypes.PHOTO)
async def get_photo_id(message: types.Message):
    sender_id = message.from_user.id
    if message.photo:
        await bot.send_photo(sender_id, photo=message.photo[-1].file_id,
                             caption=message.photo[-1].file_id)

# @dp.message_handler(lambda message: message.chat.id == operator and message.text not in all_commands,
#                     content_types=ContentTypes.ANY)
# async def forward_message(message: types.Message):
#     read = await commands.select_active_users()
#     try:
#         active_user = read.active_user_id
#         if message.photo:
#             await bot.send_photo(active_user, photo=message.photo[-1].file_id)
#         elif message.voice:
#             await bot.send_voice(active_user, voice=message.voice.file_id)
#         elif message.audio:
#             await bot.send_audio(active_user, audio=message.audio.file_id)
#         elif message.document:
#             await bot.send_document(active_user, document=message.document.file_id)
#         elif message.video:
#             await bot.send_video(active_user, video=message.video.file_id)
#         elif message.sticker:
#             await bot.send_sticker(active_user, sticker=message.sticker.file_id)
#         else:
#             await bot.send_message(active_user, message.text)
#     except:
#         await message.answer('Нет активных чатов')


# @dp.callback_query_handler(get_order.filter())
# async def get_to_work(call: types.CallbackQuery, callback_data: dict):
#     user_id = int(callback_data.get("user_id"))
#     status = callback_data.get("status")
#     message_id = callback_data.get("message_id")
#     chat_id = call.message.chat.id
#     if status == 'inwork':
#         order = await commands.select_order(user_id)
#         text_order = order.order_text
#         work_order = text_order.replace("Заказ", "<b>Взят в работу заказ</b>")
#         await call.message.edit_reply_markup()
#         await bot.send_message(2006308022, text_order, parse_mode=types.ParseMode.HTML,
#                                reply_markup=InlineKeyboardMarkup(row_width=1, inline_keyboard=[
#             [InlineKeyboardButton('Закрыть заказ', callback_data=get_order.new(user_id=user_id, status='close', message_id=message_id))]
#         ]))
#         await bot.edit_message_text(work_order, chat_id, message_id, parse_mode=types.ParseMode.HTML)
#     elif status == 'close':
#         await call.message.edit_reply_markup()
#         order = await commands.select_order(user_id)
#         text_order = order.order_text
#         close_order = text_order.replace("Заказ", "<b>Закрыт заказ</b>")
#         await bot.send_message(operator, close_order, parse_mode=types.ParseMode.HTML)
#         await bot.send_message(user_id, f'Доставлен ли Ваш {text_order}?', parse_mode=types.ParseMode.HTML,
#                                reply_markup=InlineKeyboardMarkup(row_width=1, inline_keyboard=[
#                                    [InlineKeyboardButton('Да получен', callback_data=get_delivery.new(status="got"))],
#                                    [InlineKeyboardButton('Да получен есть вопросы', callback_data=get_delivery.new(status="gotquest"))]
#                                ]))
#     else:
#         pass
#     await call.answer("Ok")
#
#
# @dp.callback_query_handler(get_delivery.filter())
# async def got_delivery(call: types.CallbackQuery, callback_data: dict):
#     await call.message.edit_reply_markup()
#     status_delivery = callback_data.get("status")
#     user_id = call.from_user.id
#     order = await commands.select_order(user_id)
#     text_order = order.order_text
#     got_order = text_order.replace("Заказ", "<b>Доставлен заказ</b>")
#     await commands.delete_order(user_id)
#     if status_delivery == "got":
#         await bot.send_message(operator, got_order, parse_mode=types.ParseMode.HTML)
#     elif status_delivery == "gotquest":
#         await bot.send_message(operator, got_order, parse_mode=types.ParseMode.HTML)
#         await call.message.answer('Напишите пожалуйста, какие вопросы у Вас возникли?')
#     else:
#         pass

# @dp.message_handler(commands=['Закрыть_чат'])
# async def stop_chat(message: types.Message):
#     await commands.close_chat()


# @dp.message_handler(commands=['Входящие_заказы'])
# async def orders_archive(message: types.Message):
#     orders = await commands.select_all_orders()
#     if orders == []:
#         await message.answer('Нет входящих заказов')
#     else:
#         for ret in orders:
#             user_id = ret.user_id
#             mess = await message.answer(text=f'{ret.order_text}\n', parse_mode=types.ParseMode.HTML)
#             await message.answer('^^^^^^^^^^^^^^^^^^^', reply_markup=InlineKeyboardMarkup().add(
#                                      InlineKeyboardButton('Взять в работу',
#                                                           callback_data=get_order.new(user_id=user_id, status='inwork',
# 															 message_id=mess.message_id))))


# @dp.message_handler(commands=['Входящие_сообщения'])
# async def message_archive(message: types.Message):
#     users = await commands.select_message_user()
#     if users == []:
#         await message.answer('Нет входящих сообщений')
#     else:
#         for ret in users:
#             incomes = await messages_db.read_inbox(ret.user_id)
#             await message.answer(f'{ret.fuLL_name} пишет')
#             for i in incomes:
#                 await message.answer(i[0])

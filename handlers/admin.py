from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from create_bot import bot
from aiogram.dispatcher.filters import Text
from handlers.states import FSMAdmin
from keyboards import admin_kb
from data_base.base_db import All_items

ID=None

#Получаем id текущего модератора
#@dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command(message : types.Message):
	global ID
	ID=message.from_user.id
	print(ID)
	print(message.chat.id)
	await bot.send_message(message.from_user.id, 'Что хозяин надо???', reply_markup=admin_kb.button_case_admin)
	await message.delete()

#Начало диалога загрузки первого пункта меню
#@dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message : types.Message):
	if message.from_user.id==ID:
		await FSMAdmin.photo.set()
		await message.reply('Загрузи фото')


#Выход из состояний
#@dp.message_handler(state="*", commands='отмена')
#@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handier(message : types.Message, state : FSMContext):
	if message.from_user.id==ID:
		current_state = await state.get_state()
		if current_state is None:
			return
		await state.finish()
		await message.reply('Ok')

#Ловим первый ответ и пишем в словарь
#@dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message : types.Message, state : FSMContext):
	if message.from_user.id==ID:
		photo = message.photo[-1].file_id
		await message.reply('Теперь введи id')
		await FSMAdmin.item_id.set()
		await state.update_data(photo=photo)

#jhkjhjh
async def load_id(message: types.Message, state : FSMContext):
	if message.from_user.id==ID:
		item_id = message.text
		await message.reply('Теперь ввкди артикул')
		await FSMAdmin.article.set()
		await state.update_data(item_id=item_id)

async def load_article(message : types.Message, state: FSMContext):
	if message.from_user.id==ID:
		article = message.text
		await message.reply('Теперь ввкди название')
		await FSMAdmin.name.set()
		await state.update_data(article=article)

#Ловим второй ответ
#@dp.message_handler(state=FSMAdmin.name)
async def load_name(message : types.Message, state : FSMContext):
	if message.from_user.id==ID:
		name = message.text
		await message.reply('Введи единицу измерения')
		await FSMAdmin.unit.set()
		await state.update_data(name=name)

async def load_unit(message: types.Message, state: FSMContext):
	if message.from_user.id==ID:
		unit = message.text
		await message.reply('Введи описание')
		await FSMAdmin.description.set()
		await state.update_data(unit=unit)

#Ловим третий ответ
#@dp.message_handler(state=FSMAdmin.description)
async def load_description(message : types.Message, state : FSMContext):
	if message.from_user.id==ID:
		description = message.text
		await message.reply('Теперь укажи цену')
		await FSMAdmin.price.set()
		await state.update_data(description=description)

#Ловим четвертый ответ
#@dp.message_handler(state=FSMAdmin.price)
async def load_price(message : types.Message, state : FSMContext):
	if message.from_user.id==ID:
		price = int(message.text)
		await message.reply('Теперь укажи оличество')
		await FSMAdmin.quantity.set()
		await state.update_data(price=price)

async def load_quatity(message: types.Message, state: FSMContext):
	if message.from_user.id == ID:
		quantity = int(message.text)
		await state.update_data(quantity=quantity)
		item = All_items()
		data = await state.get_data()
		photo = data.get('photo')
		item_id = data.get('item_id')
		name = data.get('name')
		unit = data.get('unit')
		description = data.get('description')
		price = data.get('price')
		item.photo = photo
		item.item_id = item_id
		item.name = name
		item.unit = unit
		item.description = description
		item.price = price
		await item.create()
		await state.reset_state()

#Регистрируем хендлеры
def register_handlers_admin(dp : Dispatcher):
	dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
	dp.register_message_handler(cancel_handier, state="*", commands='отмена')
	dp.register_message_handler(cancel_handier, Text(equals='отмена', ignore_case=True), state="*")
	dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
	dp.register_message_handler(load_id, state=FSMAdmin.item_id)
	dp.register_message_handler(load_article, state=FSMAdmin.article)
	dp.register_message_handler(load_name, state=FSMAdmin.name)
	dp.register_message_handler(load_unit, state=FSMAdmin.unit)
	dp.register_message_handler(load_description, state=FSMAdmin.description)
	dp.register_message_handler(load_price, state=FSMAdmin.price)
	dp.register_message_handler(load_quatity, state=FSMAdmin.quantity)
	dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
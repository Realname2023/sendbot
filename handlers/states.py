from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.callback_data import CallbackData

new_quantity = CallbackData("new_quantity", "item_id", "price")
del_item = CallbackData("del_item", "item_id")
client_order = CallbackData("get_order", "user_id")
buy_item = CallbackData("buy", "item_id", "price")
select_cat = CallbackData("sel", "cat")
select_city = CallbackData("cities", "city")
get_order = CallbackData("work", "user_id", "status", "message_id")
get_delivery = CallbackData("delivery", "status")


class FSMAdmin(StatesGroup):
    photo = State()
    item_id = State()
    article = State()
    name = State()
    unit = State()
    description = State()
    price = State()
    quantity = State()


class FSMAdmin2(StatesGroup):
    id = State()
    callback = State()
    edit_text = State()
    row_width = State()
    button_text = State()
    button_data = State()


class FSMClient(StatesGroup):
    buy_item_id = State()
    item = State()
    buy_price = State()
    buy_del_price = State()
    delivery = State()
    buy_quantity = State()
    buy_unit = State()
    city = State()
    org_name = State()
    address = State()
    phone = State()


class FSMOrder(StatesGroup):
    comment = State()
    order = State()
    new_quantity = State()
    order_item_id = State()
    order_price = State()
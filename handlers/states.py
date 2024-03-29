from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.callback_data import CallbackData

new_quantity = CallbackData("new_quantity", "user_item", "quantity", "del_quantity")
del_item = CallbackData("del_item", "item_id")
client_order = CallbackData("get_order", "user_id")
buy_item = CallbackData("buy", "item_id", "price")
select_cat = CallbackData("sel", "cat")
select_city = CallbackData("cities", "city")
get_order = CallbackData("work", "user_id", "status")
get_delivery = CallbackData("delivery", "status")


class FSMAdmin(StatesGroup):
    photo = State()
    item_id = State()
    name = State()
    unit = State()
    description = State()
    price = State()
    del_price = State()
    item_city = State()
    cat_back = State()


class FSMAdmin2(StatesGroup):
    id = State()
    callback = State()
    edit_text = State()
    row_width = State()
    button_text = State()
    button_data = State()


class FSMClient(StatesGroup):
    buy_item_id = State()
    buy_b_id = State()
    item = State()
    buy_price = State()
    buy_del_price = State()
    delivery = State()
    buy_quantity = State()
    buy_arenda_time = State()
    buy_unit = State()
    city = State()
    org_name = State()
    address = State()
    phone = State()


class FSMOrder(StatesGroup):
    comment = State()
    order = State()
    new_quantity = State()
    new_arenda_time = State()
    order_user_item = State()
    order_item_id = State()
    order_price = State()
    order_delivery = State()

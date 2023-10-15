from asyncpg import UniqueViolationError
from create_bot import bot
from data_base.gino_db import db
from data_base.base_db import User, Category,\
    Oredrs, Client, CurrentOrder, All_items

async def add_user(user_id: int, first_name: str, last_name: str, user_name: str, status: str):
    try:
        user = User(user_id=user_id, first_name=first_name, last_name=last_name, user_name=user_name, status=status)
        await user.create()
        return user
    except UniqueViolationError:
        print("Пользователь не добавлен")


async def select_all_users():
    all_users = await User.query.gino.all()
    return all_users

# async def count_users():
#     count = await db.func.count(User.user_id).gino.scalar()
#     return count

async def select_user(user_id):
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user


async def select_all_items():
    all_items = await All_items.query.gino.all()
    return all_items


async def select_item(item_id):
    item = await All_items.query.where(All_items.item_id == item_id).gino.first()
    return item


async def select_category(call_data):
    data_button = await Category.query.where(Category.callback == call_data).gino.all()
    data_button.sort(key=lambda x: x.id)
    return data_button


async def select_category_item(call_data):
    data_button = await Category.query.where(Category.callback == call_data).gino.first()
    return data_button


async def select_order(user_id):
    order = await Oredrs.query.where(Oredrs.user_id==user_id).gino.first()
    return order


async def add_order(user_id, order_text: str, status: str):
    try:
        order = Oredrs(user_id=user_id, order_text=order_text, status=status)
        await order.create()
    except UniqueViolationError:
        order = await select_order(user_id)
        order_text = order.order_text + '\n' + "=======================" + '\n' + order_text
        await order.update(order_text=order_text).apply()


async def delete_order(user_id):
    await Oredrs.delete.where(Oredrs.user_id==user_id).gino.first()


async def select_all_orders():
    orders = await Oredrs.query.gino.all()
    return orders


async def select_client(user_id):
    client = await Client.query.where(Client.user_id==user_id).gino.first()
    return client


async def add_current_order(user_id, item_id, name, unit, price, quantity, sum, city, comment = ''):
    try:
        current_order = CurrentOrder(user_id=user_id, item_id=item_id, name=name,
                                     unit=unit, price=price, quantity=quantity, sum=sum, city=city,
                                     comment=comment)
        await current_order.create()
    except UniqueViolationError:
        current_order = await CurrentOrder.query.where(CurrentOrder.user_id==user_id and CurrentOrder.item_id==item_id).gino.first()
        sum2 = current_order.sum + sum
        quantity2 = current_order.quantity + quantity
        await current_order.update(quantity=quantity2, sum=sum2).apply()


async def select_current_orders(user_id):
    current_orders = await CurrentOrder.query.where(CurrentOrder.user_id==user_id).gino.all()
    return current_orders


async def select_current_order(user_id, item_id):
    current_order = await CurrentOrder.query.where(CurrentOrder.user_id == user_id and CurrentOrder.item_id == item_id).gino.first()
    return current_order


async def delete_item_cur_order(user_id, item_id):
    current_order = await CurrentOrder.query.where(
        CurrentOrder.user_id == user_id and CurrentOrder.item_id == item_id).gino.first()
    await current_order.delete()


async def change_quantity_cur_order(user_id, item_id, new_quahtity, new_sum):
    current_order = await CurrentOrder.query.where(
        CurrentOrder.user_id == user_id and CurrentOrder.item_id == item_id).gino.first()
    await current_order.update(quantity=new_quahtity, sum=new_sum).apply()


async def set_comment(user_id, comment):
    current_order = await CurrentOrder.query.where(
        CurrentOrder.user_id == user_id).gino.first()
    comments = current_order.comment + "\n" + comment
    await current_order.update(comment=comments).apply()


async def delete_cur_order(user_id):
    await CurrentOrder.delete.where(
        CurrentOrder.user_id == user_id).gino.all()
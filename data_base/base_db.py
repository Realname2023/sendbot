from data_base.gino_db import TimedBaseModel
from sqlalchemy import Column, BigInteger, String, sql


class User(TimedBaseModel):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)
    first_name = Column(String(200))
    last_name = Column(String(200))
    user_name = Column(String(50))
    status = Column(String(30))

    query: sql.select


class Client(TimedBaseModel):
    __tablename__ = 'clients'
    user_id = Column(BigInteger, primary_key=True)
    city = Column(String(100))
    org_name = Column(String(1000))
    address = Column(String(1000))
    phone = Column(String(100))

    query: sql.select


class All_items(TimedBaseModel):
    __tablename__ = 'all_items'
    item_id = Column(String(100), primary_key=True)
    photo = Column(String(100))
    name = Column(String(200))
    unit = Column(String(100))
    description = Column(String(100000))
    price = Column(BigInteger)
    del_price = Column(BigInteger)
    city = Column(String(100))
    city_back = Column(String(100))
    b_id = Column(String(100))

    query: sql.select


# class All_products(TimedBaseModel):
#     __tablename__ = 'all_products'
#     item_id = Column(String(100), primary_key=True)
#     photo = Column(String(100))
#     name = Column(String(200))
#     unit = Column(String(100))
#     description = Column(String(100000))
#     price = Column(BigInteger)
#     del_price = Column(BigInteger)
#     city = Column(String(100))
#     city_back = Column(String(100))
#     b_id = Column(String(100))

#     query: sql.select

class Category(TimedBaseModel):
    __tablename__ = 'category_items'
    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    callback = Column(String(100))
    edit_text = Column(String(1000))
    row_width = Column(BigInteger)
    button_text = Column(String(200))
    button_data = Column(String(100))

    query: sql.select


class Oredrs(TimedBaseModel):
    __tablename__ = 'orders'
    user_id = Column(BigInteger, primary_key=True)
    order_text = Column(String(10000))
    status = Column(String(100))

    query: sql.select


class CurrentOrder(TimedBaseModel):
    __tablename__ = 'current_orders'
    user_item = Column(String(100), primary_key=True)
    user_id = Column(BigInteger)
    item_id = Column(String(100))
    b_id = Column(String(100))
    name = Column(String(100))
    unit = Column(String(100))
    price = Column(BigInteger)
    del_price = Column(BigInteger)
    quantity = Column(BigInteger)
    del_quantity = Column(BigInteger)
    arenda_time = Column(BigInteger)
    sum = Column(BigInteger)
    city = Column(String(100))
    comment = Column(String(10000))

    query: sql.select

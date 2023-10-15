from middlewares import throttling
from aiogram import Dispatcher
from .throttling import ThrottlingMiddleware

def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
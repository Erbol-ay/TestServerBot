from aiogram.dispatcher.filters.state import StatesGroup, State


class Order(StatesGroup):
    name = State()
    number = State()
    code = State()
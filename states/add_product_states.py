from aiogram.dispatcher.filters.state import StatesGroup, State


class Add_product(StatesGroup):
    name = State()
    code = State()
    file_id = State()
    point = State()
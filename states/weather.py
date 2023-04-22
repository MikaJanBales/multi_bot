from aiogram.dispatcher.filters.state import StatesGroup, State


class City(StatesGroup):
    city = State()
    fin = State()

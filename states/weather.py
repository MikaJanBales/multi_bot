from aiogram.dispatcher.filters.state import StatesGroup, State


# класс стейтов машиного состояния для функции прогноза погоды
class City(StatesGroup):
    city = State()
    fin = State()

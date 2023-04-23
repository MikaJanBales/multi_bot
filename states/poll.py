from aiogram.dispatcher.filters.state import StatesGroup, State


# класс стейтов машиного состояния для функции создания опроса
class Poll(StatesGroup):
    question = State()
    answers = State()

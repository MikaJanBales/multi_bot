from aiogram.dispatcher.filters.state import StatesGroup, State


# класс стейтов машиного состояния для функции конвертации валют
class Wallets(StatesGroup):
    sum_wallet = State()
    from_to_wallet = State()

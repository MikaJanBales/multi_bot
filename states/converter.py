from aiogram.dispatcher.filters.state import StatesGroup, State


class Wallets(StatesGroup):
    sum_wallet = State()
    from_to_wallet = State()

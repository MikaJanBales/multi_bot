from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from multi_bot.data.config import API_TELEGRAM

# Создаем переменную бота
bot = Bot(API_TELEGRAM)


storage = MemoryStorage()

# Создаем диспетчер
dp = Dispatcher(bot, storage=storage)

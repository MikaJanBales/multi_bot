from aiogram import types

from multi_bot.handlers.photo import get_photo_animal
from multi_bot.keyboards.menu_button import button_for_menu
from multi_bot.loader import dp
from multi_bot.states.converter import Wallets
from multi_bot.states.poll import Poll
from multi_bot.states.weather import City
from multi_bot.handlers.weather import get_weather_handler
from multi_bot.handlers.poll import get_question_for_poll
from multi_bot.handlers.converter import get_convert_sum_wallet


# обработчик команды "/start"
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    mess = f"Привет, {message.from_user.first_name}! Выбери, пожалуйста, функцию, чем хочешь воспользоваться."
    markup = button_for_menu()
    await message.reply(mess, reply_markup=markup)


# обработчик неожидающих сообщений от пользователя
@dp.message_handler(content_types=["text"])
async def text_handler(message: types.Message):
    mess = "Пожалуйста, выберите функцию"
    await message.reply(mess)


# обработчик inline-кнопок callback
@dp.callback_query_handler()
async def callback(call):
    if call.data == "get_weather":
        mess = "Введите название города"
        await call.message.answer(mess)
        await City.city.set()

    elif call.data == "get_photo_animal":
        await get_photo_animal(call.message)

    elif call.data == "get_convert":
        mess = "Введите сумму конвертации"
        await call.message.answer(mess)
        await Wallets.sum_wallet.set()

    elif call.data == "create_poll":
        mess = "Введите вопрос для опроса"
        await call.message.answer(mess)
        await Poll.question.set()

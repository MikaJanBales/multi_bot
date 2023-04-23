from aiogram import executor, types
from multi_bot.handlers.photo import get_photo_animal
from multi_bot.handlers.weather import get_weather_handler
from multi_bot.handlers.poll import get_question_for_poll
from multi_bot.handlers.converter import get_convert_sum_wallet
from multi_bot.loader import dp
from multi_bot.states.converter import Wallets
from multi_bot.states.poll import Poll
from multi_bot.states.weather import City


# обработчик команды "/start"
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    mess = f"Привет, {message.from_user.first_name}! Выбери, пожалуйста, функцию, чем хочешь воспользоваться."

    # создание кнопок меню
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Узнать прогноз погоды", callback_data="get_weather"))
    markup.add(types.InlineKeyboardButton("Конвертировать валюты", callback_data="get_convert"))
    markup.add(types.InlineKeyboardButton("Фото милых животных", callback_data="get_photo_animal"))
    markup.add(types.InlineKeyboardButton("Создать опрос", callback_data="create_poll"))
    await message.reply(mess, reply_markup=markup)


# обработчик inline-кнопок callback
@dp.callback_query_handler()
async def callback(call):
    if call.data == "get_weather":
        await call.message.answer("Введите название города")
        await City.city.set()

    elif call.data == "get_photo_animal":
        await get_photo_animal(call.message)

    elif call.data == "get_convert":
        await call.message.answer("Введите сумму конвертации")
        await Wallets.sum_wallet.set()

    elif call.data == "create_poll":
        await call.message.answer("Введите вопрос для опроса")
        await Poll.question.set()


# запуск бота
executor.start_polling(dp)

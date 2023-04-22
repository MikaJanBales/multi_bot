import json
import random
import requests
from aiogram import Bot, Dispatcher, executor, types

API_UNSPLASH = "btTIiFulwbe6qPUHwu5t5FYuQcgMt_Cgt-a2u21fHrg"
API_WEATHER = "e1cdd54c64df773004226ac272b0d2db"
bot = Bot("5738671159:AAHQRqZAsa956Gusn26NmKtS5QbDz-5ZcPw")
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    mess = "Привет! Выбери, пожалуйста, функцию, чем хочешь воспользоваться."
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Узнать прогноз погоды", callback_data="get_weather"))
    markup.add(types.InlineKeyboardButton("Конвертировать валюты", callback_data="get_convert"))
    markup.add(types.InlineKeyboardButton("Фото милых животных", callback_data="get_photo_animal"))
    markup.add(types.InlineKeyboardButton("Создать опрос", callback_data="regdf"))
    await message.reply(mess, reply_markup=markup)


@dp.callback_query_handler()
async def callback(call):
    if call.data == "get_weather":
        await call.message.answer("Введите название города")
    elif call.data == "get_photo_animal":
        await get_photo_animal(call.message)


@dp.message_handler(content_types=["text"])
async def get_weather(message: types.Message):
    city = message.text.strip().lower()
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_WEATHER}&units=metric")
    if res.status_code == 200:
        data = json.loads(res.text)
        await message.answer(f"Сейчас погода в городе {data['name']}: {data['main']['temp']}°C")
    else:
        await message.answer("Город указан не верно")


async def get_photo_animal(message):
    # Параметры запроса
    params = {
        "query": "cute animals",
        "orientation": "landscape",
        "count": 25,
        "client_id": API_UNSPLASH
    }

    # URL для запроса
    url = "https://api.unsplash.com/photos/random"

    # Отправляем запрос и получаем ответ
    response = requests.get(url, params=params)
    # Извлекаем URL случайной фотографии с милым животным из ответа
    data = response.json()
    random_photo = random.choice(data)
    photo_url = random_photo["urls"]["regular"]
    await message.answer_photo(photo_url)


executor.start_polling(dp)




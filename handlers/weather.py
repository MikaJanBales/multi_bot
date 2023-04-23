import json

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext

from multi_bot.data.config import API_WEATHER
from multi_bot.loader import dp
from multi_bot.states.weather import City


# хендлер для обработки названия города и выдачи прогноза погоды
@dp.message_handler(state=City.city)
async def get_weather_handler(message: types.Message, state: FSMContext):
    # сохранение ввода(название города) от пользователя
    answer = message.text
    city = answer.strip().lower()

    # URL для доступа к OpenWeatherMap API
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_WEATHER}&units=metric"

    # Отправляем GET-запрос
    res = requests.get(url)

    # Обрабатываем ответ сервера и извлекаем температуру определенного города
    if res.status_code == 200:
        data = json.loads(res.text)
        await message.answer(f"Сейчас погода в городе {data['name']}: {data['main']['temp']}°C")
    else:
        await message.answer("Город указан не верно")

    await state.finish()

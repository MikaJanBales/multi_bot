import random

import requests

from multi_bot.data.config import API_UNSPLASH


# функция для выдачи фото милого животного
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

    # Отправляем GET-запрос
    response = requests.get(url, params=params)

    # Обрабатываем ответ сервера и извлекаем URL случайной фотографии с милым животным из ответа
    if response.status_code == 200:
        data = response.json()
        random_photo = random.choice(data)
        photo_url = random_photo["urls"]["regular"]
        await message.answer_photo(photo_url)
    else:
        await message.answer("Попробуйте еще раз и сообщите, пожалуйста, администратору")
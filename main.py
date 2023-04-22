import json
import random
import requests
from aiogram import executor, types
from aiogram.dispatcher import FSMContext
from multi_bot.data.config import API_WEATHER, API_UNSPLASH, API_CONVERT
from multi_bot.loader import dp, bot
from multi_bot.states.converter import Wallets
from multi_bot.states.poll import Poll
from multi_bot.states.weather import City


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    mess = f"Привет, {message.from_user.first_name}! Выбери, пожалуйста, функцию, чем хочешь воспользоваться."
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Узнать прогноз погоды", callback_data="get_weather"))
    markup.add(types.InlineKeyboardButton("Конвертировать валюты", callback_data="get_convert"))
    markup.add(types.InlineKeyboardButton("Фото милых животных", callback_data="get_photo_animal"))
    markup.add(types.InlineKeyboardButton("Создать опрос", callback_data="create_poll"))
    await message.reply(mess, reply_markup=markup)


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


@dp.message_handler(state=Poll.question)
async def get_question_for_poll(message: types.Message, state: FSMContext):
    answer = message.text
    print(answer)
    answer += '?' if answer[-1] != '?' else answer
    await state.update_data(question=answer)
    await message.answer("Напиши варианты ответа через ';'(точку с запятой)")
    await Poll.answers.set()


@dp.message_handler(state=Poll.answers)
async def get_answers_for_poll(message: types.Message, state: FSMContext):
    answer = message.text.split(";")
    print(answer)
    await state.update_data(answers=answer)
    data = await state.get_data()
    question = data.get("question")
    answers = data.get("answers")
    print(question, answers)
    await bot.send_poll(chat_id=message.chat.id, question=question, options=answers)
    await state.finish()


async def convert(amount, from_wallet, to_wallet):
    url = f'https://v6.exchangerate-api.com/v6/{API_CONVERT}/latest/{from_wallet}'
    response = requests.get(url)
    data = response.json()
    course = data["conversion_rates"][to_wallet]
    res = round(amount * course, 2)
    return res


@dp.message_handler(state=Wallets.sum_wallet)
async def get_convert_sum_wallet(message: types.Message, state: FSMContext):
    try:
        answer = float(message.text.strip())
        await state.update_data(sum_wallet=answer)
    except ValueError:
        await message.reply("Неверный формат. Впишите сумму.")
        await Wallets.sum_wallet.set()
        return
    if float(message.text.strip()) > 0:
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        btn1 = types.KeyboardButton("RUB/USD")
        btn2 = types.KeyboardButton("RUB/EUR")
        btn3 = types.InlineKeyboardButton("USD/EUR")
        btn4 = types.InlineKeyboardButton("Другое значение.")
        markup.add(btn1, btn2, btn3, btn4)
        await message.reply("Выберите пару валют", reply_markup=markup)
        await Wallets.from_to_wallet.set()
    else:
        await message.reply("Сумма должна быть больше 0. Впишите сумму.")
        await Wallets.sum_wallet.set()


@dp.message_handler(state=Wallets.from_to_wallet)
async def get_convert_from_to_wallet(message: types.Message, state: FSMContext):
    answer = message.text
    if answer != "Другое значение.":
        answer = answer.upper().split("/")
        await state.update_data(from_to_wallet=answer)
        data = await state.get_data()
        amount = data.get("sum_wallet")
        from_wallet = data.get("from_to_wallet")[0]
        to_wallet = data.get("from_to_wallet")[1]
        try:
            res = await convert(amount, from_wallet, to_wallet)
            await message.answer(
                f"На данный момент {amount}{from_wallet} равно {res}{to_wallet}. Можете вписать сумму.")
            await Wallets.sum_wallet.set()
        except:
            await message.reply("Такая валюта не поддерживается.")
            await Wallets.sum_wallet.set()
    else:
        await message.answer("Напишите пару валют в виде <1 валюта>/<2 валюта>")
        await Wallets.from_to_wallet.set()
    # await state.finish()


@dp.message_handler(state=City.city)
async def get_weather_handler(message: types.Message, state: FSMContext):
    answer = message.text
    city = answer
    city = city.strip().lower()
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_WEATHER}&units=metric")
    if res.status_code == 200:
        data = json.loads(res.text)
        await message.answer(f"Сейчас погода в городе {data['name']}: {data['main']['temp']}°C")
    else:
        await message.answer("Город указан не верно")

    await state.finish()


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

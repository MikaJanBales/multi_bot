import requests
from aiogram import types
from aiogram.dispatcher import FSMContext

from multi_bot.data.config import API_CONVERT
from multi_bot.loader import dp
from multi_bot.states.converter import Wallets


# функция для конвертации валют
async def convert(amount, from_wallet, to_wallet):
    # URL для доступа к API Exchange Rate
    url = f'https://v6.exchangerate-api.com/v6/{API_CONVERT}/latest/{from_wallet}'

    # Отправляем GET-запрос
    response = requests.get(url)

    # Обрабатываем ответ сервера
    if response.status_code == 200:
        data = response.json()
        course = data["conversion_rates"][to_wallet]
        res = round(amount * course, 2)
        return res
    else:
        raise


# хендлер для обработки конвиртируемой суммы
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


# хендлер для обработки конвиртируемых валют и выдача результата конвертации
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

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext

from multi_bot.data.config import API_CONVERT
from multi_bot.keyboards.menu_button import button_for_menu
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


# обработчик конвиртируемой суммы
@dp.message_handler(state=Wallets.sum_wallet)
async def get_convert_sum_wallet(message: types.Message, state: FSMContext):
    # обработка ошибки на неверный ввод(не число)
    try:
        # сохранение ввода(сумму конвертации) пользователя
        answer = float(message.text.strip())
        await state.update_data(sum_wallet=answer)
    except ValueError:
        mess = "Неверный формат. Впишите сумму."
        await message.reply(mess)
        await Wallets.sum_wallet.set()
        return

    # обработка ошибки на неверный ввод(число меньше или равно нуля)
    if float(message.text.strip()) > 0:

        # создание кнопок меню
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        btn1 = types.KeyboardButton("RUB/USD")
        btn2 = types.KeyboardButton("RUB/EUR")
        btn3 = types.InlineKeyboardButton("USD/EUR")
        btn4 = types.InlineKeyboardButton("Другое значение.")
        markup.add(btn1, btn2, btn3, btn4)
        mess = "Выберите пару валют"
        await message.reply(mess, reply_markup=markup)
        await Wallets.from_to_wallet.set()
    else:
        mess = "Сумма должна быть больше 0. Впишите сумму."
        await message.reply(mess)
        await Wallets.sum_wallet.set()


# обработчик конвиртируемых валют и выдача результата конвертации
@dp.message_handler(state=Wallets.from_to_wallet)
async def get_convert_from_to_wallet(message: types.Message, state: FSMContext):
    # сохранение ввода(пары конвертируемых валют) пользователя
    answer = message.text

    # обработка кнопок
    if answer != "Другое значение.":
        answer = answer.upper().split("/")

        # обработка ошибки ввода неправильного формата
        if len(answer) < 2:
            mess = "Неправильный формат.\nНапишите пару валют в виде <1 валюта>/<2 валюта>"
            await message.answer(mess)
            await Wallets.from_to_wallet.set()
            return
        await state.update_data(from_to_wallet=answer)
        data = await state.get_data()
        amount = data.get("sum_wallet")
        from_wallet = data.get("from_to_wallet")[0]
        to_wallet = data.get("from_to_wallet")[1]

        # обработка ошибки ввода несуществующих валют
        try:
            res = await convert(amount, from_wallet, to_wallet)
            await message.answer(
                f"На данный момент {amount}{from_wallet} равно {res}{to_wallet}.")
            await state.finish()

            mess = "Выбери, пожалуйста, функцию, чем хочешь воспользоваться."
            markup = button_for_menu()
            await message.reply(mess, reply_markup=markup)
        except UnboundLocalError:
            mess = "Такая валюта не поддерживается."
            await message.reply(mess)
            await Wallets.from_to_wallet.set()
    else:
        mess = "Напишите пару валют в виде <1 валюта>/<2 валюта>"
        await message.answer(mess)
        await Wallets.from_to_wallet.set()

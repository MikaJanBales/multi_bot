from aiogram import types


# создание кнопок меню
def buttons():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Узнать прогноз погоды", callback_data="get_weather"))
    markup.add(types.InlineKeyboardButton("Конвертировать валюты", callback_data="get_convert"))
    markup.add(types.InlineKeyboardButton("Фото милых животных", callback_data="get_photo_animal"))
    markup.add(types.InlineKeyboardButton("Создать опрос", callback_data="create_poll"))
    return markup

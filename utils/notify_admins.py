import logging

from aiogram import Dispatcher

from multi_bot.data.config import admins_id


# отправка ошибок администраторам
async def on_startup_notify(dp: Dispatcher):
    for admin in admins_id:
        try:
            text = "Бот запущен"
            await dp.bot.send_message(chat_id=admin, text=text)
        except Exception as err:
            logging.exception(err)

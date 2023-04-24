from aiogram import types
from aiogram.dispatcher import FSMContext

from multi_bot.loader import dp, bot
from multi_bot.states.poll import Poll


# хендлер для обработки вопроса от пользователя
@dp.message_handler(state=Poll.question)
async def get_question_for_poll(message: types.Message, state: FSMContext):
    answer = message.text
    if answer[-1] != '?':
        answer += '?'
    await state.update_data(question=answer)
    await message.answer("Напиши варианты ответа через ';'(точку с запятой)")
    await Poll.answers.set()


# хендлер для обработки вариантов ответа от пользователя и создание опроса
@dp.message_handler(state=Poll.answers)
async def get_answers_for_poll(message: types.Message, state: FSMContext):
    answer = message.text.split(";")
    await state.update_data(answers=answer)
    data = await state.get_data()
    question = data.get("question")
    answers = data.get("answers")
    await bot.send_poll(chat_id=message.chat.id, question=question, options=answers)
    await state.finish()

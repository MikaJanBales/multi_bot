from aiogram import types
from aiogram.dispatcher import FSMContext

from multi_bot.keyboards.menu_button import button_for_menu
from multi_bot.loader import dp, bot
from multi_bot.states.poll import Poll


# обработчик вопроса от пользователя
@dp.message_handler(state=Poll.question)
async def get_question_for_poll(message: types.Message, state: FSMContext):
    answer = message.text
    if answer[-1] != '?':
        answer += '?'
    await state.update_data(question=answer)
    mess = "Напиши варианты ответа через ';'(точку с запятой)"
    await message.answer(mess)
    await Poll.answers.set()


# обработчик вариантов ответа от пользователя и создание опроса
@dp.message_handler(state=Poll.answers)
async def get_answers_for_poll(message: types.Message, state: FSMContext):
    # обработка ошибки неправильного ввода(формат)
    try:
        answer = message.text.split(";")

        # обработка ошибки неправильного ввода(вариантов ответа должно быть больше 1)
        if len(answer) < 2:
            mess = "Вариантов ответа должно быть больше одного.\nНапиши варианты ответа через ';'(точку с запятой)"
            await message.answer(mess)
            await Poll.answers.set()
        else:
            await state.update_data(answers=answer)
            data = await state.get_data()
            question = data.get("question")
            answers = data.get("answers")
            await bot.send_poll(chat_id=message.chat.id, question=question, options=answers)
            await state.finish()

            mess = "Выбери, пожалуйста, функцию, чем хочешь воспользоваться."
            markup = button_for_menu()
            await message.reply(mess, reply_markup=markup)

    except:
        mess = "Неверный формат вариантов ответа.\nНапиши варианты ответа через ';'(точку с запятой)"
        await message.answer(mess)
        await Poll.answers.set()

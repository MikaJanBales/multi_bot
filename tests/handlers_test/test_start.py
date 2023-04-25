# from unittest.mock import AsyncMock
#
# import pytest
#
# from multi_bot.handlers.start import start
# from multi_bot.keyboards.menu_button import button_for_menu
#
#
# @pytest.mark.asyncio
# async def test_start_handler():
#     message = AsyncMock()
#     await start(message)
#
#     mess = f"Привет, {message.from_user.first_name}! Выбери, пожалуйста, функцию, чем хочешь воспользоваться."
#     message.answer.assert_called_with(mess, reply_markup=button_for_menu())

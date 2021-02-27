from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import GROUP, ADMINS
from keyboards.inline.main_keyboard import main_menu
from loader import dp


# @dp.message_handler(CommandStart())
# async def bot_start(message: types.Message):
#     if str(message.chat.id) not in ADMINS:
#         await message.answer(f"Привет, {message.from_user.full_name}!",
#                             reply_markup=main_menu)
#     else:
#         await message.answer("Вы админ")

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(f"Привет, {message.from_user.full_name}!",
                         reply_markup=main_menu)
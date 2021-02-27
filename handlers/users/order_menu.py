from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.main_keyboard import back_keyboard
from loader import dp, db
from states.order_states import Order

msg_list = []
@dp.callback_query_handler(text="to_order")
async def ordering(call: CallbackQuery, state: FSMContext):
    msg = await call.message.edit_text("Введите ваше имя")
    await call.message.edit_reply_markup(back_keyboard)
    await Order.name.set()
    msg_list.append(msg)

@dp.message_handler(state=Order.name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    msg = await message.answer("Введите ваш номер",
                         reply_markup=back_keyboard)
    await Order.number.set()
    msg_list.append(msg)

@dp.message_handler(state=Order.number)
async def get_number(message: types.Message, state: FSMContext):
    number = message.text
    await state.update_data(number=number)
    msg = await message.answer("Введите код товара",
                         reply_markup=back_keyboard)
    await Order.code.set()
    msg_list.append(msg)

@dp.message_handler(state=Order.code)
async def get_code(message: types.Message, state: FSMContext):
    data = await state.get_data()
    code = message.text
    name = data.get("name")
    number = data.get("number")
    await state.finish()

    orders = await db.select_all_orders()
    if orders == []:
        await db.add_order(id=1, name=name, number=number, code=code)
    else:
        last_id = orders[-1][0]
        await db.add_order(id=last_id + 1, name=name, number=number, code=code)

    for msg in msg_list:
        await msg.delete()
    msg_list.clear()
    msg = await message.answer("Ваш заказ записан\n"
                         f"Имя: {name}\n"
                         f"Номер: {number}\n"
                         f"Код товара: {code}",
                         reply_markup=back_keyboard)
    msg_list.append(msg)
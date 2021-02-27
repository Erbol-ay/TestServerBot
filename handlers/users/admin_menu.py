import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hcode

from keyboards.inline.main_keyboard import main_menu, admin_keyboard, order_delete, back_to_admin_menu
from loader import dp, db, bot
from states.add_product_states import Add_product


@dp.callback_query_handler(text="admin")
async def admin_menu(call: CallbackQuery):
    await call.message.edit_text("Добро пожаловать")
    await call.message.edit_reply_markup(admin_keyboard)

order_list = []
@dp.callback_query_handler(text="show_orders")
async def showing_orders(call: CallbackQuery):

    await call.answer()
    orders = await db.select_all_orders()
    for order in order_list:
        await order.delete()
    order_list.clear()
    print(order_list)

    if orders == []:
        msg = await call.message.answer("Нет заказов")
        order_list.append(msg)
    else:
        for order in orders:
            order = await call.message.answer(hcode("id: {id}\n"
                                            "Имя: {name}\n"
                                            "Номер: {number}\n"
                                            "Код товара: {code}".format(**order)),
                                              reply_markup=order_delete)
            order_list.append(order)

@dp.callback_query_handler(text="delete_order")
async def delete_this_order(call: CallbackQuery):
    await call.answer()
    match = re.search(r'id\D\s\d+', call.message.text)
    match = re.search(r'\d+', match[0])
    id = int(match[0])
    await db.delete_order(id=id)
    if call.message in order_list:
        order_list.remove(call.message)
    await call.message.delete()


product_msgs = []


@dp.callback_query_handler(text="back_admin")
@dp.callback_query_handler(text="back_admin", state=Add_product.all_states)
async def get_back(call: CallbackQuery, state: FSMContext):
    await state.finish()
    for msg in product_msgs:
        await msg.delete()
    product_msgs.clear()
    await call.message.answer("Добро пожаловать",
                              reply_markup=admin_keyboard)


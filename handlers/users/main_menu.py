from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from handlers.users.admin_menu import order_list
from handlers.users.admin_product_part import product_list
from handlers.users.order_menu import msg_list
from keyboards.inline.main_keyboard import main_menu
from loader import dp
from states.order_states import Order


@dp.callback_query_handler(text="back")
@dp.callback_query_handler(text="back", state=Order.all_states)
async def main_keyboard(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(f"Привет {call.from_user.full_name}")
    await call.message.edit_reply_markup(main_menu)
    for product in product_list:
        await product.delete()
    product_list.clear()

    for order in order_list:
        await order.delete()
    order_list.clear()

    if msg_list != []:
        msg_list.pop()

    for msg in msg_list:
        await msg.delete()

    msg_list.clear()
    await state.finish()
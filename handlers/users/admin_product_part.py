import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hcode

from handlers.users.admin_menu import product_msgs
from keyboards.inline.main_keyboard import back_to_admin_menu, product_delete
from loader import dp, db, bot
from states.add_product_states import Add_product

product_list = []
@dp.callback_query_handler(text="show_products")
async def showing_orders(call: CallbackQuery):
    await call.answer()
    products = await db.select_all_products()
    for order in product_list:
        await order.delete()
    product_list.clear()

    if products == []:
        msg = await call.message.answer("Нет товаров")
        product_list.append(msg)

    for product in products:
        print(product)
        type = product[5]
        if type == "photo":
            product = await bot.send_photo(chat_id=call.from_user.id,
                                           photo=product[3],
                                           caption=hcode("id: {id}\n"
                                                         "Название: {name}\n"
                                                         "Код товара: {code}\n"
                                                         "Балл товара: {point}".format(**product)),
                                           reply_markup=product_delete)
        else:
            product = await bot.send_video(chat_id=call.from_user.id,
                                           video=product[3],
                                           caption=hcode("id: {id}\n"
                                                         "Название: {name}\n"
                                                         "Код товара: {code}\n"
                                                         "Балл товара: {point}".format(**product)),
                                           reply_markup=product_delete)
        product_list.append(product)

@dp.callback_query_handler(text="delete_product")
async def delete_this_order(call: CallbackQuery):
    await call.answer()
    print(call.message.caption)
    match = re.search(r'id\D\s\d+', call.message.caption)
    match = re.search(r'\d+', match[0])
    id = int(match[0])
    await db.delete_product(id=id)
    if call.message in product_list:
        product_list.remove(call.message)
    await call.message.delete()


@dp.callback_query_handler(text="add_product")
async def add_new_product(call: CallbackQuery, state: FSMContext):
    msg = await call.message.edit_text("Введите название товара")
    await call.message.edit_reply_markup(back_to_admin_menu)
    await Add_product.name.set()
    product_msgs.append(msg)

@dp.message_handler(state=Add_product.name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    msg = await message.answer("Введите код товара",
                            reply_markup=back_to_admin_menu)
    await Add_product.code.set()
    product_msgs.append(msg)

@dp.message_handler(state=Add_product.code)
async def get_code(message: types.Message, state: FSMContext):
    code = message.text
    await state.update_data(code=code)
    msg = await message.answer("Отправьте фото или видео товара\n"
                               "Примечание: При отправке фото, не снимайте галочку с 'Compress images'\n"
                               "А если там нет галочки, ставьте галочку перед отправкой",
                               reply_markup=back_to_admin_menu)
    await Add_product.file_id.set()
    product_msgs.append(msg)

@dp.message_handler(state=Add_product.file_id, content_types=types.ContentTypes.PHOTO)
async def get_photo(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await state.update_data(file_id=file_id)
    await state.update_data(type="photo")
    msg = await message.answer("Введите балл товара")
    await Add_product.point.set()
    product_msgs.append(msg)

@dp.message_handler(state=Add_product.file_id, content_types=types.ContentTypes.VIDEO)
async def get_video(message: types.Message, state: FSMContext):
    file_id = message.video.file_id
    await state.update_data(file_id=file_id)
    await state.update_data(type="video")
    msg = await message.answer("Введите балл товара")
    await Add_product.point.set()
    product_msgs.append(msg)

@dp.message_handler(state=Add_product.point)
async def get_count(message: types.Message, state: FSMContext):
    point = int(message.text)
    data = await state.get_data()
    name = data.get("name")
    code = data.get("code")
    file_id = data.get("file_id")
    type = data.get("type")
    await state.finish()

    products = await db.select_all_products()
    if products == []:
        await db.add_product(id=1, name=name, code=code, file_id=file_id, point=point, type=type)
    else:
        last_id = products[-1][0]
        await db.add_product(id=last_id+1, name=name, code=code, file_id=file_id, point=point, type=type)

    for msg in product_msgs:
        await msg.delete()
    product_msgs.clear()

    msg = await message.answer(f"Добавлен новый товар",
                               reply_markup=back_to_admin_menu)
    if type == "photo":
        msg2 = await bot.send_photo(chat_id=message.from_user.id,
                                    photo=file_id,
                                    caption=f"Название: {name}\n"
                                            f"Код товара: {code}\n"
                                            f"Балл: {point}")
    else:
        msg2 = await bot.send_video(chat_id=message.from_user.id,
                             video=file_id,
                             caption=f"Название: {name}\n"
                                     f"Код товара: {code}\n"
                                     f"Балл: {point}")

    product_msgs.append(msg)
    product_msgs.append(msg2)
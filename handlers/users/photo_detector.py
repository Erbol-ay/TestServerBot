# from aiogram import types
#
# from loader import dp, db, bot
#
#
# @dp.message_handler(content_types=types.ContentTypes.PHOTO)
# async def get_photo_id(message: types.Message):
#     await db.add_product(id=1, name=message.from_user.full_name, code=str(message.from_user.id), file_id=message.photo[-1].file_id)
#     product = await db.select_product(id=1)
#     await bot.send_photo(chat_id=message.from_user.id,
#                          photo=product[3],
#                          caption=f"Name: {product[1]}\n"
#                                  f"Code: {product[2]}\n"
#                                  f"Count: {product[4]}")
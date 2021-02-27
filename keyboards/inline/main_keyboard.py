from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



main_menu = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Информация",
                                 callback_data="info")
        ],
        [
            InlineKeyboardButton(text="Каталог",
                                 callback_data="catalog")
        ],
        [
            InlineKeyboardButton(text="Заказать",
                                 callback_data="to_order")
        ],
        [
            InlineKeyboardButton(text="Рекомендованные товары",
                                 callback_data="recommended_products")
        ],
        [
            InlineKeyboardButton(text="Администратор",
                                 callback_data="admin")
        ]
    ]
)

back_keyboard = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад",
                                 callback_data="back"
            )
        ]
    ]
)

admin_keyboard = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Посмотреть заказы",
                                 callback_data="show_orders"),
            InlineKeyboardButton(text="Посмотреть товары",
                                 callback_data="show_products")
        ],
        [
            InlineKeyboardButton(text="Добавить товар",
                                 callback_data="add_product")
        ],
        [
            InlineKeyboardButton(text="Удалить несколько заказов",
                                 callback_data="delete_some_orders"),
            InlineKeyboardButton(text="Удалить несколько товаров",
                                 callback_data="delete_some_products")
        ],
        [
            InlineKeyboardButton(text="Удалить все заказы",
                                 callback_data="delete_all_orders"),
            InlineKeyboardButton(text="Удалить все товары",
                                 callback_data="delete_all_products")
        ],
        [
            InlineKeyboardButton(text="Назад",
                                 callback_data="back")
        ]
    ]
)

order_delete = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Удалить заказ",
                                 callback_data="delete_order")
        ]
    ]
)

product_delete = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Удалить товар",
                                 callback_data="delete_product")
        ]
    ]
)

back_to_admin_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад",
                                 callback_data="back_admin")
        ]
    ]
)
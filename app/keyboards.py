from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Показать производительность по количеству приказов',
                          callback_data='action_1')],
    [InlineKeyboardButton(text='Показать производительность по количеству баллов',
                          callback_data='action_2')]
])

menu_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Количество пользователей', callback_data='number_of_users')],
    [InlineKeyboardButton(text='Список пользователей', callback_data='list_of_users')]
])

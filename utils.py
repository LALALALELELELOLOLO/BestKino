import random
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from constants import users, genres, greetings


def get_name(msg_or_query):
    if hasattr(msg_or_query, 'from_user'):
        username = msg_or_query.from_user.username
    else:
        username = msg_or_query.username
    return users.get(username, username or "друг")


def get_greetings():
    return random.choice(greetings)

#keyboard = InlineKeyboardMarkup(row_width=2,inline_keyboard=[])
keyboard = InlineKeyboardMarkup(row_width=2,inline_keyboard=[[InlineKeyboardButton(text="😂 Комедия", callback_data="comedy")],
    [InlineKeyboardButton(text="💥 Боевик", callback_data="action")],
    [InlineKeyboardButton(text="😱 Ужасы", callback_data="horror")],
    [InlineKeyboardButton(text="❤️ Мелодрама", callback_data="love")],
    [InlineKeyboardButton(text="🕵️ Детектив", callback_data="detective")]])
'''keyboard.add(
    InlineKeyboardButton(text="😂 Комедия", callback_data="comedy"),
    InlineKeyboardButton(text="💥 Боевик", callback_data="action"),
    InlineKeyboardButton(text="😱 Ужасы", callback_data="horror"),
    InlineKeyboardButton(text="❤️ Мелодрама", callback_data="love"),
    InlineKeyboardButton(text="🕵️ Детектив", callback_data="detective")
)'''
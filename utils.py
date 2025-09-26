import random
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from constants import users, texts, drinks


def get_name(msg_or_query):
    if hasattr(msg_or_query, 'from_user'):
        username = msg_or_query.from_user.username
    else:
        username = msg_or_query.username
    return users.get(username, username or "друг")


def get_greetings():
    return random.choice(texts)

keyboard = InlineKeyboardMarkup(row_width=2)
keyboard.add(
    InlineKeyboardButton("😂 Комедия", callback_data="comedy"),
    InlineKeyboardButton("💥 Боевик", callback_data="action"),
    InlineKeyboardButton("😱 Ужасы", callback_data="horror"),
    InlineKeyboardButton("❤️ Мелодрама", callback_data="love"),
    InlineKeyboardButton("🕵️ Детектив", callback_data="detective")
)
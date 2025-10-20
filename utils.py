import random
import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from annotated_types.test_cases import cases
from random import randrange

from constants import users, greetings, page_size

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_name(msg_or_query):
    if hasattr(msg_or_query, 'from_user'):
        username = msg_or_query.from_user.username
    else:
        username = msg_or_query.username
    return users.get(username, username or "друг")


def get_greetings():
    return random.choice(greetings)

genres_keyboard = InlineKeyboardMarkup(row_width=2,inline_keyboard=[[InlineKeyboardButton(text="😂 Комедия", callback_data="comedy")],
    [InlineKeyboardButton(text="💥 Боевик", callback_data="action")],
    [InlineKeyboardButton(text="😱 Ужасы", callback_data="horror")],
    [InlineKeyboardButton(text="❤️ Мелодрама", callback_data="love")],
    [InlineKeyboardButton(text="🕵️ Детектив", callback_data="detective")]])

years_keyboard = InlineKeyboardMarkup(row_width=2,inline_keyboard=[[InlineKeyboardButton(text="Свежачок", callback_data="new")],
    [InlineKeyboardButton(text="Относительно недавнее", callback_data="middle")],
    [InlineKeyboardButton(text="Старенькое", callback_data="old")],
    [InlineKeyboardButton(text="Древнее, как мумия", callback_data="too_old")]])

sort_keyboard = InlineKeyboardMarkup(row_width=2,inline_keyboard=[[InlineKeyboardButton(text="Топовые", callback_data="good")],
    [InlineKeyboardButton(text="Лучшие с конца", callback_data="bad")]])

def set_kino_filter(genre, year, sort):
    match genre:
        case 'comedy':
            genre = 'комедия'
        case 'action':
            genre = 'боевик'
        case 'horror':
            genre = 'ужасы'
        case 'love':
            genre = 'мелодрама'
        case 'detective':
            genre = 'детектив'
    match year:
        case 'new':
            year = '2024-2025'
        case 'middle':
            year = '1995-2024'
        case 'old':
            year = '1980-1994'
        case 'too_old':
            year = '1930-1979'
    match sort:
        case 'good':
            sort = '1'
        case 'bad':
            sort = '-1'
    url = f'https://api.kinopoisk.dev/v1.4/movie?page=1&limit={page_size}&selectFields(0)=name&selectFields(1)=description$selectFields(2)=poster&sortField=externalId.imdb&sortType={sort}&type=movie&status=completed&year={year}&genres.name={genre}'
    return url

async def send_recommendation(query, bot, kino_resp):
    if kino_resp["total"] == 0:
        await bot.send_message(query.from_user.id, 'Дурацкий конопоиск ничего не нашел(((')
    else:
        counter = randrange(kino_resp["total"])
        logger.info(f"Counter: {counter}")
        await bot.send_message(query.from_user.id, 'Смотрел уже этот шедевр?')
        if kino_resp["docs"][counter]["name"] is None:
            await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["alternativeName"])
        else:
            await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["name"])
        if kino_resp["docs"][counter]["poster"]["previewUrl"] is not None:
            await bot.send_photo(query.from_user.id, kino_resp["docs"][counter]["poster"]["previewUrl"])
        if kino_resp["docs"][counter]["description"] is not None:
            await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["description"])
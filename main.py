import logging
import requests

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram import F

from config import TOKEN, PATCHED_URL, KINOPOISK_TOKEN
from constants import greetings, genres
from utils import get_name, get_greetings, keyboard


#setattr(api, "API_URL", PATCHED_URL)

bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dp.message(Command('start', 'help'))
async def start_command(msg):
    user = get_name(msg)
    logger.info(f"Пользователь {user} (@{msg.from_user.username}) запустил команду: {msg.text}")

    welcome_msg = f"Привет, {user}! 👋\n\nЯ бот, который поможет тебе выбрать фильм на вечер! 🎬\n\nНапиши мне приветствие, заполни короткую анкету, и я покажу тебе варианты!"
    await msg.answer(welcome_msg, reply_markup=keyboard)

    logger.info(f"Отправил приветственное сообщение пользователю {user}")


#@dp.message(Text(equals=greetings, ignore_case=True))
@dp.message(F.text.in_(greetings))
async def greet(msg):
    user = get_name(msg)
    logger.info(f"Получено приветствие от пользователя: {user} (@{msg.from_user.username}) - сообщение: '{msg.text}'")

    greeting = get_greetings()
    logger.info(f"Отправляю приветствие пользователю {user}: '{greeting}'")

    await msg.answer(f"{greeting}, {user}")
    await msg.answer('Какой твой любимый жанр?', reply_markup=keyboard)

    logger.info(f"Показываю клавиатуру с жанрами пользователю {user}")


@dp.callback_query(F.text.in_(genres))
async def mood_callback(query):
    data = query.data
    user = get_name(query)
    logger.info(f"Пользователь {user} (@{query.from_user.username}) выбрал жанр: {data}")

    if data == 'комедия':
        logger.info(f"Рекомендую комедию пользователю {user}")
        await bot.send_message(query.from_user.id, f'ищу лучшие комедии для тебя, {user}')
        r = requests.get('https://api.kinopoisk.dev/v1.4/movie?page=1&limit=1&selectFields(0)=name&selectFields(1)=description$selectFields(2)=poster&sortField=externalId.imdb&sortType=-1&type=movie&status=completed&year=1990-2025&genres.name=Комедия', headers={"X-API-KEY":KINOPOISK_TOKEN})
        kino_resp = r.json()
        logger.info(f"Ответ кинопоиска: {kino_resp}")
        await bot.send_message(query.from_user.id,'Смотрел уже этот шедевр?')
        if kino_resp["docs"][0]["name"] is None:
            await bot.send_message(query.from_user.id, kino_resp["docs"][0]["alternativeName"])
        else:
            await bot.send_message(query.from_user.id, kino_resp["docs"][0]["name"])
        await bot.send_photo(query.from_user.id, kino_resp["docs"][0]["previewUrl"])
        if kino_resp["docs"][0]["description"] is not None:
            await bot.send_message(query.from_user.id, kino_resp["docs"][0]["description"])



@dp.message()
async def handle_other_messages(msg):
    user = get_name(msg)
    logger.info(f"Получено неизвестное сообщение от {user} (@{msg.from_user.username}): '{msg.text}'")
    logger.info(f"Игнорирую сообщение от {user}")


if __name__ == '__main__':
    logger.info("Запускаю бота...")
    dp.start_polling(bot)
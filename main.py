import logging
import requests
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram import F
from random import randrange

from config import TOKEN, PATCHED_URL, KINOPOISK_TOKEN
from constants import greetings, genres, page_size
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

    welcome_msg = f"Я бот, который поможет тебе выбрать фильм на вечер! 🎬\n\nНапиши мне приветствие, заполни короткую анкету, и я покажу тебе варианты!"
    #await msg.answer(welcome_msg, reply_markup=keyboard)
    await msg.answer(welcome_msg)

    logger.info(f"Отправил приветственное сообщение пользователю {user}")


@dp.message(F.text.in_(greetings))
async def greet(msg):
    user = get_name(msg)
    logger.info(f"Получено приветствие от пользователя: {user} (@{msg.from_user.username}) - сообщение: '{msg.text}'")

    greeting = get_greetings()
    logger.info(f"Отправляю приветствие пользователю {user}: '{greeting}'")

    await msg.answer(f"{greeting}, {user}")
    await msg.answer('Какой твой любимый жанр?', reply_markup=keyboard)

    logger.info(f"Показываю клавиатуру с жанрами пользователю {user}")


@dp.callback_query(F.data.in_(genres))
async def genres_callback(query):
    data = query.data
    user = get_name(query)
    logger.info(f"Пользователь {user} (@{query.from_user.username}) выбрал жанр: {data}")
    counter = randrange(page_size)

    if data == 'comedy':
        logger.info(f"Рекомендую комедию пользователю {user}")
        await bot.send_message(query.from_user.id, f'ищу лучшие комедии для тебя, {user}')
        #await bot.answer_callback_query(query.id,'ищу лучшие комедии для тебя, {user}')
        r = requests.get(f'https://api.kinopoisk.dev/v1.4/movie?page=1&limit={page_size}&selectFields(0)=name&selectFields(1)=description$selectFields(2)=poster&sortField=externalId.imdb&sortType=-1&type=movie&status=completed&year=1990-2025&genres.name=комедия', headers={"X-API-KEY":KINOPOISK_TOKEN})
        logger.info(r.request.url)
        logger.info(r.request.body)
        logger.info(r.request.headers)
        kino_resp = r.json()
        logger.info(f"Ответ кинопоиска: {kino_resp}")
        await bot.send_message(query.from_user.id,'Смотрел уже этот шедевр?')
        if kino_resp["docs"][counter]["name"] is None:
            await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["alternativeName"])
        else:
            await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["name"])
        await bot.send_photo(query.from_user.id, kino_resp["docs"][counter]["poster"]["previewUrl"])
        if kino_resp["docs"][counter]["description"] is not None:
            await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["description"])
    if data == 'action':
        logger.info(f"Рекомендую Боевик {user}")
        await bot.send_message(query.from_user.id, f'ищу лучшие боевики')
        r = requests.get(f'https://api.kinopoisk.dev/v1.4/movie?page=1&limit={page_size}&selectFields(0)=name&selectFields(1)=description$selectFields(2)=poster&sortField=externalId.imdb&sortType=-1&type=movie&status=completed&year=1990-2025&genres.name=боевик', headers={"X-API-KEY": KINOPOISK_TOKEN})
        logger.info(r.request.url)
        logger.info(r.request.body)
        logger.info(r.request.headers)
        kino_resp = r.json()
        logger.info(f"Ответ кинопоиска: {kino_resp}")
        await bot.send_message(query.from_user.id, 'Видел этот фильм?')
        if kino_resp["docs"][counter]["name"] is None:
            await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["alternativeName"])
        else:
            await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["name"])
        await bot.send_photo(query.from_user.id, kino_resp["docs"][counter]["poster"]["previewUrl"])
        if kino_resp["docs"][counter]["description"] is not None:
            await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["description"])
    if data == 'horror':
        logger.info(f"Рекомендую Ужас {user}")
        await bot.send_message(query.from_user.id, f'Посмотрим что может тебя напугать')
        r = requests.get(f'https://api.kinopoisk.dev/v1.4/movie?page=1&limit={page_size}&selectFields(0)=name&selectFields(1)=description$selectFields(2)=poster&sortField=externalId.imdb&sortType=-1&type=movie&status=completed&year=1990-2025&genres.name=ужасы', headers={"X-API-KEY": KINOPOISK_TOKEN})
        logger.info(r.request.url)
        logger.info(r.request.body)
        logger.info(r.request.headers)
        kino_resp = r.json()
        logger.info(f"Ответ кинопоиска: {kino_resp}")
        await bot.send_message(query.from_user.id, 'Тебе знаком этот фильм?')
        if kino_resp["docs"][counter]["name"] is None:
            await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["alternativeName"])
        else:
            await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["name"])
        await bot.send_photo(query.from_user.id, kino_resp["docs"][counter]["poster"]["previewUrl"])
        if kino_resp["docs"][counter]["description"] is not None:
            await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["description"])
            if data == 'love':
        logger.info(f"Рекомендую мелодраму {user}")
        await bot.send_message(query.from_user.id, f'Давай найдем тебе классный фильм на вечер')
        r = requests.get(f'https://api.kinopoisk.dev/v1.4/movie?page=1&limit={page_size}&selectFields(0)=name&selectFields(1)=description$selectFields(2)=poster&sortField=externalId.imdb&sortType=-1&type=movie&status=completed&year=1990-2025&genres.name=мелодрама', headers={"X-API-KEY": KINOPOISK_TOKEN})
        logger.info(r.request.url)
        logger.info(r.request.body)
        logger.info(r.request.headers)
        kino_resp = r.json()
        logger.info(f"Ответ кинопоиска: {kino_resp}")
        await bot.send_message(query.from_user.id, 'Самое то для хорошего вечера!')
        if kino_resp["docs"][counter]["name"] is None:
            await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["alternativeName"])
        else:
            await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["name"])
        await bot.send_photo(query.from_user.id, kino_resp["docs"][counter]["poster"]["previewUrl"])
        if kino_resp["docs"][counter]["description"] is not None:
            await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["description"])
        if    data == 'detective':
            logger.info(f"Рекомендую детектив {user}")
            await bot.send_message(query.from_user.id, f'Готов к делу, Детектив {user}?')
            r = requests.get(
                f'https://api.kinopoisk.dev/v1.4/movie?page=1&limit={page_size}&selectFields(0)=name&selectFields(1)=description$selectFields(2)=poster&sortField=externalId.imdb&sortType=-1&type=movie&status=completed&year=1990-2025&genres.name=детективы', headers={"X-API-KEY": KINOPOISK_TOKEN})
            logger.info(r.request.url)
            logger.info(r.request.body)
            logger.info(r.request.headers)
            kino_resp = r.json()
            logger.info(f"Ответ кинопоиска: {kino_resp}")
            await bot.send_message(query.from_user.id, 'Раскроем это дело?')
            if kino_resp["docs"][counter]["name"] is None:
                await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["alternativeName"])
            else:
                await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["name"])
            await bot.send_photo(query.from_user.id, kino_resp["docs"][counter]["poster"]["previewUrl"])
            if kino_resp["docs"][counter]["description"] is not None:
                await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["description"])
@dp.message()
async def handle_other_messages(msg):
    user = get_name(msg)
    logger.info(f"Получено неизвестное сообщение от {user} (@{msg.from_user.username}): '{msg.text}'")
    logger.info(f"Игнорирую сообщение от {user}")


#if __name__ == '__main__':
#    logger.info("Запускаю бота...")
#    dp.start_polling(bot)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logger.info("Запускаю бота...")
    asyncio.run(main())

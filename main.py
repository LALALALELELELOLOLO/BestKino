import logging
import requests
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram import F
from random import randrange

from config import TOKEN, PATCHED_URL, KINOPOISK_TOKEN
from constants import greetings, genres, years, sort, page_size
from utils import get_name, get_greetings, genres_keyboard, years_keyboard, sort_keyboard, set_kino_filter, send_recommendation

#setattr(api, "API_URL", PATCHED_URL)

bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
counter = randrange(page_size)


@dp.message(Command('start', 'help'))
async def start_command(msg):
    user = get_name(msg)
    logger.info(f"Пользователь {user} (@{msg.from_user.username}) запустил команду: {msg.text}")

    welcome_msg = f"Я бот, который поможет тебе выбрать фильм на вечер! 🎬\n\nНапиши мне приветствие, заполни короткую анкету, и я покажу тебе варианты!"
    #await msg.answer(welcome_msg, reply_markup=keyboard)
    await msg.answer(welcome_msg)

    logger.info(f"Отправил приветственное сообщение пользователю {user}")


@dp.message(F.text.lower().in_(greetings))
async def greet(msg):
    user = get_name(msg)
    logger.info(f"Получено приветствие от пользователя: {user} (@{msg.from_user.username}) - сообщение: '{msg.text}'")
    greeting = get_greetings()
    logger.info(f"Отправляю приветствие пользователю {user}: '{greeting}'")
    await msg.answer(f"{greeting}, {user}")
    await msg.answer('Какой твой любимый жанр?', reply_markup=genres_keyboard)
    logger.info(f"Показываю клавиатуру с жанрами пользователю {user}")

@dp.callback_query(F.data.in_(genres))
async def genres_callback(query):
    genre_data = query.data
    user = get_name(query)
    logger.info(f"Пользователь {user} (@{query.from_user.username}) выбрал жанр: {genre_data}")
    #await msg.answer('А что по дате выхода фильма?', reply_markup=years_keyboard)
    await bot.send_message(query.from_user.id, 'А что по дате выхода фильма?', reply_markup=years_keyboard)
    logger.info(f"Показываю клавиатуру с годами пользователю {user}")
    @dp.callback_query(F.data.in_(years))
    async def years_callback(query):
        year_data = query.data
        user = get_name(query)
        logger.info(f"Пользователь {user} (@{query.from_user.username}) выбрал годы: {year_data}")
        #await msg.answer('Какой рейтинг интересует?', reply_markup=sort_keyboard)
        await bot.send_message(query.from_user.id, 'Какой рейтинг интересует?', reply_markup=sort_keyboard)
        logger.info(f"Показываю клавиатуру с сортировкой пользователю {user}")
        @dp.callback_query(F.data.in_(sort))
        async def sort_callback(query):
            sort_data = query.data
            user = get_name(query)
            logger.info(f"Пользователь {user} (@{query.from_user.username}) выбрал сортировку: {sort_data}")
            r = requests.get(set_kino_filter(genre_data, year_data, sort_data), headers={"X-API-KEY": KINOPOISK_TOKEN})
            logger.info(r.request.url)
            logger.info(r.request.body)
            logger.info(r.request.headers)
            kino_resp = r.json()
            logger.info(f"Ответ кинопоиска: {kino_resp}")
            await send_recommendation(query, bot, kino_resp, counter)

    # if genre_data == 'comedy':
    #     logger.info(f"Рекомендую комедию пользователю {user}")
    #     await bot.send_message(query.from_user.id, f'ищу лучшие комедии для тебя, {user}')
    #     #r = requests.get(f'https://api.kinopoisk.dev/v1.4/movie?page=1&limit={page_size}&selectFields(0)=name&selectFields(1)=description$selectFields(2)=poster&sortField=externalId.imdb&sortType=1&type=movie&status=completed&year=1990-2025&genres.name=комедия', headers={"X-API-KEY":KINOPOISK_TOKEN})
    #
    #     r = requests.get(set_kino_filter(genre_data,year_data,sort_data), headers={"X-API-KEY":KINOPOISK_TOKEN})
    #     logger.info(r.request.url)
    #     logger.info(r.request.body)
    #     logger.info(r.request.headers)
    #     kino_resp = r.json()
    #     logger.info(f"Ответ кинопоиска: {kino_resp}")
    #     #send_recommendation(bot,kino_resp)
    #     if kino_resp["total"] == 0:
    #         await bot.send_message(query.from_user.id, 'Дурацкий конопоиск ничего не нашел(((')
    #     else:
    #         if kino_resp["total"] < counter:
    #             counter = randrange(kino_resp["total"])
    #         logger.info(f"Counter: {counter}")
    #         await bot.send_message(query.from_user.id, 'Смотрел уже этот шедевр?')
    #         if kino_resp["docs"][counter]["name"] is None:
    #             await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["alternativeName"])
    #         else:
    #             await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["name"])
    #         if kino_resp["docs"][counter]["poster"]["previewUrl"] is not None:
    #             await bot.send_photo(query.from_user.id, kino_resp["docs"][counter]["poster"]["previewUrl"])
    #         if kino_resp["docs"][counter]["description"] is not None:
    #             await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["description"])
    # if genre_data == 'action':
    #     logger.info(f"Рекомендую Боевик {user}")
    #     await bot.send_message(query.from_user.id, f'ищу лучшие боевики')
    #     r = requests.get(f'https://api.kinopoisk.dev/v1.4/movie?page=1&limit={page_size}&selectFields(0)=name&selectFields(1)=description$selectFields(2)=poster&sortField=externalId.imdb&sortType=1&type=movie&status=completed&year=1990-2025&genres.name=боевик', headers={"X-API-KEY": KINOPOISK_TOKEN})
    #     logger.info(r.request.url)
    #     logger.info(r.request.body)
    #     logger.info(r.request.headers)
    #     kino_resp = r.json()
    #     logger.info(f"Ответ кинопоиска: {kino_resp}")
    #     if kino_resp["total"] == 0:
    #         await bot.send_message(query.from_user.id, 'Дурацкий конопоиск ничего не нашел(((')
    #     else:
    #         if kino_resp["total"] < counter:
    #             counter = randrange(kino_resp["total"])
    #         logger.info(f"Counter: {counter}")
    #         await bot.send_message(query.from_user.id, 'Видел этот фильм?')
    #         if kino_resp["docs"][counter]["name"] is None:
    #             await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["alternativeName"])
    #         else:
    #             await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["name"])
    #         if kino_resp["docs"][counter]["poster"]["previewUrl"] is not None:
    #             await bot.send_photo(query.from_user.id, kino_resp["docs"][counter]["poster"]["previewUrl"])
    #         if kino_resp["docs"][counter]["description"] is not None:
    #             await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["description"])
    # if genre_data == 'horror':
    #     logger.info(f"Рекомендую Ужас {user}")
    #     await bot.send_message(query.from_user.id, f'Посмотрим что может тебя напугать')
    #     r = requests.get(f'https://api.kinopoisk.dev/v1.4/movie?page=1&limit={page_size}&selectFields(0)=name&selectFields(1)=description$selectFields(2)=poster&sortField=externalId.imdb&sortType=1&type=movie&status=completed&year=1990-2025&genres.name=ужасы', headers={"X-API-KEY": KINOPOISK_TOKEN})
    #     logger.info(r.request.url)
    #     logger.info(r.request.body)
    #     logger.info(r.request.headers)
    #     kino_resp = r.json()
    #     logger.info(f"Ответ кинопоиска: {kino_resp}")
    #     if kino_resp["total"] == 0:
    #         await bot.send_message(query.from_user.id, 'Дурацкий конопоиск ничего не нашел(((')
    #     else:
    #         if kino_resp["total"] < counter:
    #             counter = randrange(kino_resp["total"])
    #         logger.info(f"Counter: {counter}")
    #         await bot.send_message(query.from_user.id, 'Тебе знаком этот фильм?')
    #         if kino_resp["docs"][counter]["name"] is None:
    #             await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["alternativeName"])
    #         else:
    #             await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["name"])
    #         if kino_resp["docs"][counter]["poster"]["previewUrl"] is not None:
    #             await bot.send_photo(query.from_user.id, kino_resp["docs"][counter]["poster"]["previewUrl"])
    #         if kino_resp["docs"][counter]["description"] is not None:
    #             await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["description"])
    # if genre_data == 'love':
    #     logger.info(f"Рекомендую мелодраму {user}")
    #     await bot.send_message(query.from_user.id, f'Найдем лучший фильм на вечер')
    #     r = requests.get(f'https://api.kinopoisk.dev/v1.4/movie?page=1&limit={page_size}&selectFields(0)=name&selectFields(1)=description$selectFields(2)=poster&sortField=externalId.imdb&sortType=1&type=movie&status=completed&year=1990-2025&genres.name=мелодрама', headers={"X-API-KEY": KINOPOISK_TOKEN})
    #     logger.info(r.request.url)
    #     logger.info(r.request.body)
    #     logger.info(r.request.headers)
    #     kino_resp = r.json()
    #     logger.info(f"Ответ кинопоиска: {kino_resp}")
    #     if kino_resp["total"] == 0:
    #         await bot.send_message(query.from_user.id, 'Дурацкий конопоиск ничего не нашел(((')
    #     else:
    #         if kino_resp["total"] < counter:
    #             counter = randrange(kino_resp["total"])
    #         logger.info(f"Counter: {counter}")
    #         await bot.send_message(query.from_user.id, 'Сгодится для хорошего вечера?')
    #         if kino_resp["docs"][counter]["name"] is None:
    #             await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["alternativeName"])
    #         else:
    #             await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["name"])
    #         if kino_resp["docs"][counter]["poster"]["previewUrl"] is not None:
    #             await bot.send_photo(query.from_user.id, kino_resp["docs"][counter]["poster"]["previewUrl"])
    #         if kino_resp["docs"][counter]["description"] is not None:
    #             await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["description"])
    # if genre_data == 'detective' :
    #     logger.info(f"Рекомендую детектив {user}")
    #     await bot.send_message(query.from_user.id, f'ищу лучший детектив...')
    #     r = requests.get(f'https://api.kinopoisk.dev/v1.4/movie?page=1&limit={page_size}&selectFields(0)=name&selectFields(1)=description$selectFields(2)=poster&sortField=externalId.imdb&sortType=1&type=movie&status=completed&year=1990-2025&genres.name=детектив',  headers={"X-API-KEY": KINOPOISK_TOKEN})
    #     logger.info(r.request.url)
    #     logger.info(r.request.body)
    #     logger.info(r.request.headers)
    #     kino_resp = r.json()
    #     logger.info(f"Ответ кинопоиска: {kino_resp}")
    #     if kino_resp["total"] == 0:
    #         await bot.send_message(query.from_user.id, 'Дурацкий конопоиск ничего не нашел(((')
    #     else:
    #         if kino_resp["total"] < counter:
    #             counter = randrange(kino_resp["total"])
    #         logger.info(f"Counter: {counter}")
    #         await bot.send_message(query.from_user.id, 'Готов раскрыть это дело?')
    #         if kino_resp["docs"][counter]["name"] is None:
    #             await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["alternativeName"])
    #         else:
    #             await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["name"])
    #         if kino_resp["docs"][counter]["poster"]["previewUrl"] is not None:
    #             await bot.send_photo(query.from_user.id, kino_resp["docs"][counter]["poster"]["previewUrl"])
    #         if kino_resp["docs"][counter]["description"] is not None:
    #             await bot.send_message(query.from_user.id, kino_resp["docs"][counter]["description"])

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

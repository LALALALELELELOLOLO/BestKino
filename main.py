import aiogram
import datetime
import logging

from aiogram.utils.executor import start_polling
from aiogram import Bot, Dispatcher
from aiogram.bot import api
from aiogram.dispatcher.filters import Command, Text

from config import TOKEN, PATCHED_URL
from constants import greetings, genres
from utils import get_name, get_greetings, keyboard

setattr(api, "API_URL", PATCHED_URL)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dp.message_handler(Command(['start', 'help']))
async def start_command(msg):
    user = get_name(msg)
    logger.info(f"Пользователь {user} (@{msg.from_user.username}) запустил команду: {msg.text}")

    welcome_msg = f"Привет, {user}! 👋\n\nЯ бот, который поможет тебе выбрать фильм на вечер! 🍻\n\nНапиши мне приветствие, заполни короткую анкету, и я покажу тебе варианты!"
    await msg.answer(welcome_msg, reply_markup=keyboard)

    logger.info(f"Отправил приветственное сообщение пользователю {user}")


@dp.message_handler(Text(equals=greetings, ignore_case=True))
async def greet(msg):
    user = get_name(msg)
    logger.info(f"Получено приветствие от пользователя: {user} (@{msg.from_user.username}) - сообщение: '{msg.text}'")

    greeting = get_greetings()
    logger.info(f"Отправляю приветствие пользователю {user}: '{greeting}'")

    await msg.answer(f"{greeting}, {user}")
    await msg.answer('Какой твой любимый жанр?', reply_markup=keyboard)

    logger.info(f"Показываю клавиатуру с жанрами пользователю {user}")


@dp.callback_query_handler(Text(equals=genres))
async def mood_callback(query):
    data = query.data
    user = get_name(query)
    logger.info(f"Пользователь {user} (@{query.from_user.username}) выбрал жанр: {data}")

    if data == 'комедия':
        logger.info(f"Рекомендую комедию пользователю {user}")
        await bot.send_message(query.from_user.id, f'я думаю, что тебе нужно винишко, {user}')
        await bot.send_message(query.from_user.id,
                               'смотри, что я для тебя нашел - https://edadeal.ru/moskva/offers?segment=wine')
    elif data == 'боевик':
        logger.info(f"Рекомендую боевик пользователю {user}")
        await bot.send_message(query.from_user.id, 'для тебя сейчас самое оно - текила!')
        await bot.send_message(query.from_user.id,
                               'тут короче есть скидоны - https://edadeal.ru/moskva/offers?segment=tequila')
    elif data == 'ужасы':
        logger.info(f"Рекомендую ужасы пользователю {user} (сочувствую!)")
        await bot.send_message(query.from_user.id, 'сочувствую')
        await bot.send_message(query.from_user.id,
                               'вот тут глянь, может что поможет - https://edadeal.ru/moskva/offers?segment=vodka')
    elif data == 'мелодрама':
        logger.info(f"Рекомендую мелодрамму пользователю {user}")
        await bot.send_message(query.from_user.id, 'у меня есть кое-что для тебя')
        await bot.send_message(query.from_user.id,
                               'даже скидочка есть - https://edadeal.ru/moskva/offers?segment=whiskey')
        await bot.send_message(query.from_user.id, f'{user}, только не забудь взять колу')
    elif data == 'детектив':
        logger.info(f"Рекомендую детектив пользователю {user}")
        await bot.send_message(query.from_user.id, 'ну вот и отлично! сейчас будет еще лучше')
        await bot.send_message(query.from_user.id, 'хорошего вечера тебе')
        await bot.send_message(query.from_user.id, 'https://edadeal.ru/moskva/offers?segment=other-alcohols')



@dp.message_handler()
async def handle_other_messages(msg):
    user = get_name(msg)
    logger.info(f"Получено неизвестное сообщение от {user} (@{msg.from_user.username}): '{msg.text}'")
    logger.info(f"Игнорирую сообщение от {user}")


if __name__ == '__main__':
    logger.info("Запускаю бота...")
    start_polling(dp, skip_updates=True)
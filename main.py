#import aiogram
import datetime
import logging

from aiogram.utils.executor import start_polling
from aiogram import Bot, Dispatcher
from aiogram.bot import api
from aiogram.dispatcher.filters import Command, Text

from config import TOKEN, PATCHED_URL
from constants import greetings, buhat, drinks
from utils import get_name, get_greetings, keyboard

setattr(api, "API_URL", PATCHED_URL)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dp.message_handler(Text(equals=greetings, ignore_case=True))
async def greet(msg):
    greeting = get_greetings()
    user = get_name(msg)
    await msg.answer(f"{greeting}, {user}")
    await msg.answer('Как твои дела сегодня?', reply_markup=keyboard)


@dp.message_handler(Text(equals=buhat, ignore_case=True))
async def send(msg):
    user = get_name(msg)
    await msg.answer('ну го, чё')
    await msg.answer_photo("http://picscomment.com/pics/3690.jpg")
    await msg.answer('Как твои дела сегодня?', reply_markup=keyboard)


@dp.callback_query_handler(Text(equals=drinks))
async def mood_callback(query):
    data = query.data
    if data == 'vinishko':
        await bot.send_message(query.from_user.id, f'я думаю, что тебе нужно винишко, {get_name(query)}')
        await bot.send_message(query.from_user.id, 'смотри, что я для тебя нашел - https://edadeal.ru/moskva/offers?segment=wine')
    elif data == 'tequila':
        await bot.send_message(query.from_user.id, 'для тебя сейчас самое оно - текила!')
        await bot.send_message(query.from_user.id, 'тут короче есть скидоны - https://edadeal.ru/moskva/offers?segment=tequila')
    elif data == 'vodochka':
        await bot.send_message(query.from_user.id, 'сочувствую')
        await bot.send_message(query.from_user.id, 'вот тут глянь, может что поможет - https://edadeal.ru/moskva/offers?segment=vodka')
    elif data == 'viskarik':
        await bot.send_message(query.from_user.id, 'у меня есть кое-что для тебя')
        await bot.send_message(query.from_user.id, 'даже скидочка есть - https://edadeal.ru/moskva/offers?segment=whiskey')
        await bot.send_message(query.from_user.id, f'{get_name(query)}, только не забудь взять колу')
    elif data == 'rom':
        await bot.send_message(query.from_user.id, 'ну вот и отлично! сейчас будет еще лучше')
        await bot.send_message(query.from_user.id, 'хорошего вечера тебе')
        await bot.send_message(query.from_user.id,'https://edadeal.ru/moskva/offers?segment=other-alcohols')

if __name__ == '__main__':
    start_polling(dp, skip_updates=True)
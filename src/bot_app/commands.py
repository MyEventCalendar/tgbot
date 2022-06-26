from aiogram import types
from .app import dp
from . import messages
from .data_fetcher import ApiController


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    telegram_id = message.from_user.id
    username = message.from_user.username
    add_user = {"telegram_id": str(telegram_id), "username": username, " password": "12345678"}
    ApiController().post_user(add_user)
    await message.reply(messages.WELCOME_MESSAGE)

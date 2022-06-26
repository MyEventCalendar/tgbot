from aiogram import types
from aiogram.utils import markdown as md
from .app import dp
from .data_fetcher import ApiController
from . import messages

"""Структура ответа пользователю"""
LC_MAP = {
    "pk": "ID",
    "name": "Событие",
    "description": "Описание",
    "start_time": "Начало",
    "end_time": "Окончание",
    "hidden": "Признак скрытия",
    "user": "Телеграм ID"
}


@dp.message_handler(commands='actual_events')
async def actual_events(message: types.Message):
    telegram_id = message.from_user.id
    password = 12345678
    api = ApiController()
    api.make_headers(telegram_id, password)
    """Возвращает список актуальных событий из БД"""
    try:
        res = api.get_actual_events()
        if not res:
            await message.reply(messages.NO_ACTUAL_EVENTS)
        else:
            text = ""
            for event in res:
                event.pop('user')
                for event_field in event:
                    text += f"{LC_MAP[event_field]} : {md.hbold(event[event_field])}\n"
            await message.reply(text, parse_mode="HTML")
    except Exception:
        await message.reply(messages.API_SERVICE_ERROR)

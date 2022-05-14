from aiogram import types
from aiogram.utils import markdown as md
from .app import dp
from .data_fetcher import API_Metods

"""Структура ответа пользователю"""
LC_MAP = {
    "pk": "ID",
    "name": "Событие",
    "description": "Описание",
    "start_time": "Начало",
    "end_time": "Окончание",
}


@dp.message_handler(commands='actual_events')
async def actual_events(message: types.Message):
    """Возвращает список актуальных событий из БД"""
    res = API_Metods().get_actual_events()
    text = ""
    for event in res:
        for event_field in event:
            text += f"{LC_MAP[event_field]} : {md.hbold(event[event_field])}\n"
    await message.reply(text, parse_mode="HTML")


"""Система диалогов для удаления события из БД"""
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from .app import dp
from .data_fetcher import ApiController
from . import messages


class FSMDelete(StatesGroup):
    delete = State()


@dp.message_handler(commands='delete_event', state=None)
async def delete_event(message: types.Message):
    """Запускает хранение состояний"""
    await FSMDelete.delete.set()
    await message.reply(messages.REQUEST_ID)


@dp.message_handler(state=FSMDelete.delete)
async def load_id(message: types.Message, state: FSMContext):
    """Ловит ID в ответе пользователя, реализует метод delelte"""
    telegram_id = message.from_user.id
    password = 12345678
    api = ApiController()
    api.make_headers(telegram_id, password)
    async with state.proxy() as data:
        data['pk'] = message.text
        res = api.delete_event(data['pk'])
        if res == {"detail": "Not found."}:
            await message.reply(messages.DELETE_NOT_FOUND)
        else:
            await message.reply(f"Событие ID:{data['pk']} успешно удалено!")
    await state.finish()

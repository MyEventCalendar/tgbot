"""Система диалогов для изменения события в БД"""
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from .app import dp
from .data_fetcher import ApiController
from . import messages
from .keyboards import inline_kb


class FSMChange(StatesGroup):
    """Структура состояний"""
    id = State()
    poll = State()
    change = State()


@dp.message_handler(commands=['change_event'], state=None)
async def change_event(message: types.Message):
    """Запускает хранение состояний"""
    await FSMChange.id.set()
    await message.reply(messages.REQUEST_ID)


@dp.message_handler(state=FSMChange.id)
async def load_id(message: types.Message, state: FSMContext):
    """Посредством инлйн клавиатуры запрашивает у пользователя тип изменений"""
    async with state.proxy() as data:
        data['pk'] = message.text
    await FSMChange.next()
    await message.reply("Выберите пункт:", reply_markup=inline_kb)


@dp.callback_query_handler(lambda c: c.data in ['name', 'description',
                                                'start_time', 'end_time'], state=FSMChange.poll)
async def button_click_call_back(callback_query: types.CallbackQuery, state: FSMContext):
    """Ловит callback нажатой кнопки, запрашвает изменения у пользователя"""
    answer = callback_query.data
    async with state.proxy() as data:
        data[answer] = ''
        await FSMChange.next()
    if answer == 'name' or answer == 'description':
        await callback_query.message.answer(messages.CHANGE_TEXT)
    elif answer == 'start_time' or answer == 'end_time':
        await callback_query.message.answer(messages.ADD_CHANGE_EVENT_TIME)


@dp.message_handler(state=FSMChange.change)
async def load_end_time(message: types.Message, state: FSMContext):
    """Ловит изменения, реализует метод PUT, возвращает ID события"""
    telegram_id = message.from_user.id
    password = 12345678
    api = ApiController()
    api.make_headers(telegram_id, password)
    async with state.proxy() as data:
        key = list(data.keys())[-1]
        data[key] += f'{message.text}'
        try:
            res = api.put_change_event(data['pk'], data.items())
            await message.reply(f"Событие ID:{res['pk']} успешно изменено")
        except Exception:
            await message.reply(messages.API_SERVICE_ERROR)
    await state.finish()



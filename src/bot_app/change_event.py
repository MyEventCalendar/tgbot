"""Система диалогов для изменения события в БД"""
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from .app import dp
from .data_fetcher import API_Metods
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
    async with state.proxy() as data:
        data['pk'] = message.text
    await FSMChange.next()
    await message.reply(data)
    await message.reply("Выберите пункт:", reply_markup=inline_kb)


@dp.callback_query_handler(lambda c: c.data in ['name', 'description',
                                                'start_time', 'end_time'], state=FSMChange.poll)
async def button_click_call_back(callback_query: types.CallbackQuery, state: FSMContext):
    answer = callback_query.data
    async with state.proxy() as data:
        data[answer] = ''
        await FSMChange.next()
        await callback_query.message.answer(data)
    if answer == 'name' or answer == 'description':
        await callback_query.message.answer("Введите изменения")
    elif answer == 'start_time' or answer == 'end_time':
        await callback_query.message.answer("Введите новые дату и время в формате YYYY-MM-DD HH:MM")


@dp.message_handler(state=FSMChange.change)
async def load_end_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        key = list(data.keys())[-1]
        data[key] += f'{message.text}'
        res = API_Metods().put_change_event(data['pk'], data.items())
        await message.reply(f"Событие ID:{res['pk']} успешно изменено")
    await state.finish()



from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_button_name = InlineKeyboardButton('Изменить название', callback_data='name')
inline_button_description = InlineKeyboardButton('Изменить описание', callback_data='description')
inline_button_start_time = InlineKeyboardButton('Изменить дату и время начала', callback_data='start_time')
inline_button_end_time = InlineKeyboardButton('Изменить дату и время окончания', callback_data='end_time')

inline_kb = InlineKeyboardMarkup()

inline_kb.add(inline_button_name, inline_button_description)
inline_kb.add(inline_button_start_time)
inline_kb.add(inline_button_end_time)

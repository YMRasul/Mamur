from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from config import ADMIN

def main_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="📚 ReportAll"),
         KeyboardButton(text="📚 ReportDay")],
        [KeyboardButton(text="📚 PreviousMonth"),
         KeyboardButton(text="📚 ReportMonth")]
    ]
    if user_telegram_id==ADMIN:
        kb_list.append([KeyboardButton(text="⚙️ Админ панель")])
    #keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True,input_field_placeholder="Воспользуйтесь меню:")
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)

    return keyboard

def calendar_kb():
    kb = [
        [
            KeyboardButton(text='Dialog Calendar'),                   # Шуниси керак
        ],
    ]
    key_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return key_kb

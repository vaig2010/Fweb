from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

kb_remove = ReplyKeyboardRemove()
kb_main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Создать план"),
            KeyboardButton(text="Показать план")
        ],
        [
            KeyboardButton(text="План тренировок"),
            KeyboardButton(text="План питания"),
        ],
        [
            KeyboardButton(text="Удалить план"),
            KeyboardButton(text="Удалить инфу о себе"),
        ],
    ],
    resize_keyboard=True
)

kb_registration = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отмена")
        ]
    ],
    resize_keyboard=True
)

def get_keyboard(
    *btns: str,
    placeholder: str = None,
    sizes: tuple[int] = (2,),
):
    kb = ReplyKeyboardBuilder()
    for btn in btns:
        kb.add(KeyboardButton(text=btn))
    return kb.adjust(*sizes).as_markup(input_field_placeholder=placeholder, resize_keyboard=True)

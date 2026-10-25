from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕ Добавить задачу"),
            KeyboardButton(text="📋 Мои задачи"),
        ],
        [
            KeyboardButton(text="✅ Выполнить задачу"),
            KeyboardButton(text="🗑 Удалить задачу")
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выбери действие..."
)
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def task_keyboard(task_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Выполнить",
                    callback_data=f"done:{task_id}"
                ),
                InlineKeyboardButton(
                    text="🗑 Удалить",
                    callback_data=f"delete:{task_id}"
                )
            ]
        ]
    )
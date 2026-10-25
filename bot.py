import asyncio
import os
import random
from database import init_db, add_task, get_tasks, complete_task, delete_task
from keyboards.main_menu import main_menu
from keyboards.task_actions import task_keyboard
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

class AddTask(StatesGroup):
    waiting_for_text = State()

class DoneTask(StatesGroup):
    waiting_for_id = State()

class DeleteTask(StatesGroup):
    waiting_for_id = State()

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command("cancel"))
async def cancel_action(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        await message.answer("Сейчас нечего отменять.")
        return

    await state.clear()
    await message.answer(
        "❌ Действие отменено.",
        reply_markup=main_menu
        )

async def show_tasks(message: Message):
    tasks = await get_tasks(message.from_user.id)

    if not tasks:
        await message.answer("📭 У тебя пока нет задач.")
        return

    await message.answer("📋 Твои задачи:")

    for task_id, task_text, is_done in tasks:
        status = "Выполненно ✅" if is_done else "В процесе⏳"

        await message.answer(
            f"{task_id}. {task_text}: {status} ",
            reply_markup=task_keyboard(task_id)
        )

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Привет! Я TaskBot - Твой менеджер задач.\n" \
        "/help - помощь",
        reply_markup=main_menu
        )

@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer("Я умею хранить твои задачи!\n\n" \
    "/start - Запустить бота\n" \
    "/help - Справка\n"
    "/add (Текст) - Сохранить задачу\n"
    "/list - Просматривать задачи\n"
    "/done (Номер задачи) - Отметить задачу выполненной\n"
    "/delete (Номер задачи) - Удалить задачу\n"
    "/cancel - Отменить действие")

@dp.message(Command("add"))
async def add_text(message: Message):
    text = (message.text or "").partition(" ")[2].strip()
    if not text:
        await message.answer(
        "Укажи текст задачи\n" \
        "Пример: /add Купить продукты"
        )
        return
    await add_task(message.from_user.id, text)
    await message.answer(f"✅ Задача сохранена: {text}")

@dp.message(Command("list"))
async def list_tasks(message: Message):
    await show_tasks(message)

@dp.message(Command("done"))
async def done_handler(message: Message):
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer("Использование: /done (Номер задачи)")
        return

    task_id = int(parts[1])
    success = await complete_task(message.from_user.id, task_id)

    if success:
        await message.answer(f"Задача №{task_id} выполнена! ✅")
    else:
        await message.answer("Задача не найдена! ❌")

@dp.message(Command("delete"))
async def delete_handler(message: Message):
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer("Использование: /delete (Номер задачи)")
        return

    task_id = int(parts[1])
    success = await delete_task(message.from_user.id, task_id)

    if success:
        await message.answer(f"Задача №{task_id} удалена! ✅")
    else:
        await message.answer("Задача не найдена! ❌")

@dp.message(F.text == "➕ Добавить задачу")
async def start_add_task(message: Message, state: FSMContext):
    await state.set_state(AddTask.waiting_for_text)
    await message.answer("Напиши текст новой задачи:")

@dp.message(AddTask.waiting_for_text, F.text)
async def save_task_from_menu(message: Message, state: FSMContext):
    text = message.text.strip()
    if not text:
        await message.answer("Текст задачи не может быть пустым.")
        return
    await add_task(message.from_user.id, text)
    await state.clear()
    await message.answer(f"✅ Задача сохранена: {text}")

@dp.message(F.text == "📋 Мои задачи")
async def list_tasks_button(message: Message):
    await show_tasks(message)

@dp.message(F.text == "✅ Выполнить задачу")
async def start_complete_task(message: Message, state: FSMContext):
    await state.set_state(DoneTask.waiting_for_id)
    await message.answer("Напиши номер задачи, которую хочешь отметить выполненной:")

@dp.message(DoneTask.waiting_for_id, F.text)
async def done_task_from_menu(message: Message, state: FSMContext):
    try:
        task_id = int(message.text)
    except ValueError:
        await message.answer("Номер должен быть числом!\n"
        "Попробуй ещё раз!")
        return

    success = await complete_task(message.from_user.id, task_id)
    if success:
        await message.answer(f"Задача №{task_id} выполнена! ✅")
        await state.clear()
    else:
        await message.answer("Задача не найдена! ❌")

@dp.message(F.text == "🗑 Удалить задачу")
async def start_complete_task(message: Message, state: FSMContext):
    await state.set_state(DeleteTask.waiting_for_id)
    await message.answer("Напиши номер задачи, которую хочешь удалить:")

@dp.message(DeleteTask.waiting_for_id, F.text)
async def delete_task_from_menu(message: Message, state: FSMContext):
    try:
        task_id = int(message.text)
    except ValueError:
        await message.answer("Номер должен быть числом!\n"
        "Попробуй ещё раз!")
        return

    success = await delete_task(message.from_user.id, task_id)
    if success:
        await message.answer(f"Задача №{task_id} удалена! ✅")
        await state.clear()
    else:
        await message.answer("Задача не найдена! ❌")

@dp.callback_query(F.data.startswith("done:"))
async def done_task_button(callback: CallbackQuery):
    task_id = int(callback.data.split(":")[1])

    success = await complete_task(
        callback.from_user.id,
        task_id
    )

    if success:
        await callback.message.edit_text(
            f"✅ Задача #{task_id} выполнена!"
        )
    else:
        await callback.answer(
            "Задача не найдена.",
            show_alert=True
        )
        return

    await callback.answer()


@dp.callback_query(F.data.startswith("delete:"))
async def delete_task_button(callback: CallbackQuery):
    task_id = int(callback.data.split(":")[1])

    success = await delete_task(
        callback.from_user.id,
        task_id
    )

    if success:
        await callback.message.edit_text(
            f"🗑 Задача #{task_id} удалена."
        )
    else:
        await callback.answer(
            "Задача не найдена.",
            show_alert=True
        )
        return

    await callback.answer()

@dp.message(StateFilter(None), F.text)
async def random_answer(message: Message):
    answers = [
        "Круто!",
        "Очуметь!",
        "Зашибись!",
        "Да нууу нафиг!",
    ]
    await message.answer(random.choice(answers))


async def main():
    await init_db()
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
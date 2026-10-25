# TaskBot — Telegram Task Manager

A Telegram bot for managing personal tasks, built with Python and aiogram 3.

## Features

- Add tasks using commands or a keyboard menu
- View your task list
- Mark tasks as completed
- Delete tasks
- Store tasks in an SQLite database
- Use FSM to handle task creation
- Cancel an action with `/cancel`
- Keep each user's tasks private

## Technologies

- Python
- aiogram 3
- SQLite
- aiosqlite
- python-dotenv

## Setup

1. Clone or download this repository.
2. Create and activate a virtual environment.
3. Install dependencies:

   pip install -r requirements.txt

4. Create a `.env` file in the project root and add your Telegram bot token:

   BOT_TOKEN=your_telegram_bot_token

5. Start the bot:

   python bot.py

## Available Commands

- `/start` — Start the bot
- `/help` — Show available commands
- `/add <task>` — Add a task
- `/list` — Show your tasks
- `/done <id>` — Complete a task
- `/delete <id>` — Delete a task
- `/cancel` — Cancel the current action

## Notes

- The SQLite database is created automatically when the bot starts.
- Keep your bot token private.

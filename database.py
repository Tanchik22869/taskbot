import aiosqlite

DB_NAME = "tasks.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS tasks  (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                is_done INTEGER DEFAULT 0
            )
        """)
        await db.commit()

async def add_task(user_id: int, text: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO tasks (user_id, text) VALUES (?, ?)",
            (user_id, text)
        )
        await db.commit()

async def get_tasks(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT id, text, is_done FROM tasks WHERE user_id = ?",
            (user_id,)
        )
        return await cursor.fetchall()

async def complete_task(user_id, task_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
        UPDATE tasks
        SET is_done = 1
        WHERE id = ? AND user_id = ? AND is_done = 0
        """,
        (task_id, user_id)
        )
        await db.commit()
        return cursor.rowcount > 0

async def delete_task(user_id, task_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
        DELETE FROM tasks
        WHERE id = ? AND user_id = ?
        """,
        (task_id, user_id)
        )
        await db.commit()
        return cursor.rowcount > 0
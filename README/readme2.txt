import aiosqlite

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def __aenter__(self):
        self.conn = await aiosqlite.connect(self.db_path)
        self.conn.row_factory = aiosqlite.Row  # Позволяет получать результаты в виде словарей
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()

    async def execute(self, query: str, params: tuple = ()):  
        """Выполняет запрос без возврата данных (INSERT, UPDATE, DELETE)."""
        async with self.conn.cursor() as cursor:
            await cursor.execute(query, params)
        await self.conn.commit()

    async def fetchone(self, query: str, params: tuple = ()):  
        """Выполняет запрос и возвращает одну строку."""
        async with self.conn.cursor() as cursor:
            await cursor.execute(query, params)
            return await cursor.fetchone()

    async def fetchall(self, query: str, params: tuple = ()):  
        """Выполняет запрос и возвращает все строки."""
        async with self.conn.cursor() as cursor:
            await cursor.execute(query, params)
            return await cursor.fetchall()

# Пример использования
async def main():
    async with Database("database.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
        await db.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
        user = await db.fetchone("SELECT * FROM users WHERE name = ?", ("Alice",))
        print(dict(user))  # Выведет {'id': 1, 'name': 'Alice'}

# Запуск main() внутри asyncio.run(), если требуется

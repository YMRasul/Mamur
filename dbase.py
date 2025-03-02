import aiosqlite   #pip install aiosqlite
import asyncio
from config import DBASE

'''
CREATE TABLE users (
    telegid  INTEGER NOT NULL
                     PRIMARY KEY,
    fullname TEXT,
    operid   INTEGER NOT NULL,
    vvod     INTEGER DEFAULT 0,
    report   INTEGER DEFAULT 0
);
CREATE TABLE record (
    id         INTEGER NOT NULL
                       PRIMARY KEY,
    rasxid     INTEGER NOT NULL,
    smm        NUMERIC DEFAULT 0,
    datarecord TEXT,
    prim       TEXT,
    iduser     INTEGER NOT NULL,

    FOREIGN KEY (rasxid)  REFERENCES users (telegid) 
);
'''
async def dbase_start():
    async with DbaseBot(DBASE) as db:
        s = "PRAGMA foreign_keys = ON"
        await db.execute(s)
        s = 'CREATE TABLE IF NOT EXISTS users ( telegid INTEGER NOT NULL PRIMARY KEY,fullname TEXT,' \
            'operid INTEGER NOT NULL,vvod integer default 0,report integer default 0)'
        await db.execute(s)

        s = 'CREATE TABLE IF NOT EXISTS record ( id INTEGER NOT NULL PRIMARY KEY, rasxid INTEGER not null,smm NUMERIC default 0,' \
            'datarecord TEXT,prim TEXT,iduser INTEGER NOT NULL, FOREIGN KEY(rasxid) REFERENCES users(telegid))'
        await db.execute(s)

class DbaseBot:
    def __init__(self, db_file):
        self.db_file = db_file
        self.lock = asyncio.Lock()

    async def __aenter__(self):
        self.conn = await aiosqlite.connect(self.db_file)
        self.conn.row_factory = aiosqlite.Row  # Позволяет получать результаты в виде словарей
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.conn.close()

    async def check_user(self, telegram_id: int):
        async with self.lock:
            s = "SELECT telegid FROM users WHERE telegid = ?"
            async with self.conn.execute(s, (telegram_id,)) as cursor:
                user_exist = await cursor.fetchone()
            await self.conn.commit()
            return bool(user_exist)

    async def add_user(self,telegram_id: int, name,operid: int):
        async with self.lock:
            s = 'INSERT INTO users (telegid,fullname,operid) VALUES (?,?,?)'
            async with self.conn.execute(s, (telegram_id,name,operid,)) as cursor:
                await self.conn.commit()

    async def execute(self, query: str, params: tuple = ()):
        """Выполняет запрос без возврата данных (INSERT, UPDATE, DELETE)."""
        async with self.conn.cursor() as cursor:
            await cursor.execute(query, params)
            #print(f'{query} {params}')
        await self.conn.commit()

    async def fetch_one(self, query: str, params: tuple = ()):
        """Выполняет запрос и возвращает одну строку."""
        async with self.conn.cursor() as cursor:
            await cursor.execute(query, params)
            return await cursor.fetchone()

    async def fetch_all(self, query: str, params: tuple = ()):
        """Выполняет запрос и возвращает все строки."""
        async with self.conn.cursor() as cursor:
            await cursor.execute(query, params)
            return await cursor.fetchall()
'''
async def myfunc():
    async with DbaseBot(DBASE) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
        await db.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
        user = await db.fetch_one("SELECT * FROM users WHERE name = ?", ("Alice",))
        print(dict(user))  # Выведет {'id': 1, 'name': 'Alice'}
'''

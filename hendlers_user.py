from aiogram import F, Router  # F - это magic фильтр
from aiogram.types import Message
from dbase import DbaseBot
from config import DBASE,ADMIN
from datetime import datetime,timedelta

def get_routerUser(bot):
    routerUser = Router()
    #========================== del id ================================
    @routerUser.message(F.text.lower().startswith('del'))  # Удаление записи
    async def delrecord(message: Message):
        s = message.text[4:].strip()
        ms = [i.strip() for i in s.split(',')]
        tup = (int(ms[0]),)
        #del id
        try:
            async with DbaseBot(DBASE) as db:
                st = "SELECT iduser FROM  record WHERE id==?"
                record = await db.fetch_one(st, tup)  # Ищем удаляемого записи

                if record is None:
                    await message.answer(f'Record number {tup} not exist!')
                else:
                    if (record[0]==message.from_user.id):
                        st = 'DELETE FROM record WHERE id==?'
                        await db.execute(st, tup)
                        sd = f'Record number {tup} is deleted'
                        await message.answer(sd)
                        await bot.send_message(ADMIN, sd)
                        await bot.send_message(ADMIN, f'Deleted by {message.from_user.id}: {message.from_user.full_name}')
                    else:
                        sd = f'Record number {tup} is not deleted'
                        await message.answer(sd)
                        await bot.send_message(ADMIN, sd)
                        await bot.send_message(ADMIN, f'Попытка {message.from_user.id}: {message.from_user.full_name}')
        except:
            await message.answer(f'Ошибка при удаление записи: {tup}')
    # ============== ins smm,datatime,prim ==================================
    @routerUser.message(F.text.lower().startswith("ins")) # Добавление записи
    async def apprecord(message: Message):
        s = message.text[4:].strip()
        ms = [i.strip() for i in s.split(',')]
        id = message.from_user.id
        async with DbaseBot(DBASE) as db:
            s = "SELECT operid,vvod FROM users WHERE telegid = ?"
            cur = await db.fetch_one(s, (id,)) # Получаем настройки для id
            if cur[1]==1: # Если имеет право на ввод данных cur[0]
                #app  smm, date, time, prim
                x = tofloat(ms[0],id)
                if x[0]:
                    tup = (cur[0],x[1],ms[1],ms[2],id,)
                    s ="INSERT INTO record (rasxid,smm,datarecord,prim,iduser) VALUES (?,?,?,?,?)"
                    await db.execute(s, tup)

                    if x[1] < 0:
                        sd = f'Rashod:  {tup[1]} {tup[2]} {tup[3]}'
                    else:
                        sd = f'Popolnenie:  {tup[1]} {tup[2]} {tup[3]}'
                    await message.answer(sd)
                    if id==ADMIN:
                        await bot.send_message(cur[0], sd)
                        await bot.send_message(cur[0], f'Inserted by {message.from_user.id}: {message.from_user.full_name}')
                    else:
                        await bot.send_message(ADMIN, sd)
                        await bot.send_message(ADMIN, f'Inserted by {message.from_user.id}: {message.from_user.full_name}')
                else:
                    await message.answer(f' {x[1]} строка не может быть преобразована во float')
            else:
                await message.answer(f"Komanda ins sizga mumkin emas.")

    @routerUser.message(F.text.lower().startswith("upd")) # Добавление записи
    async def updrecord(message: Message):
        s = message.text
        n = len(s)
        i = 0
        while i < n:
            if s[i] == ' ':
                break
            else:
                i = i + 1
        if (i == n):
            await message.answer("Noto'g'ri komanda")
            return
        ss = s[i:].strip()
        ms = [i.strip() for i in ss.split(',')]
        id = message.from_user.id
        async with DbaseBot(DBASE) as db:
            s = "SELECT operid,vvod FROM users WHERE telegid = ?"
            cur = await db.fetch_one(s, (id,)) # Получаем настройки для id
            if cur[1]==1: # Если имеет право на изменение cur[0]
                #upd idrecord,text
                tup = (ms[1],ms[0],)
                try:
                    st = 'UPDATE record SET prim==? WHERE id==?'
                    await db.execute(st, tup)
                    await message.answer(f'Успешное изменения данных {tup}')
                    await bot.send_message(ADMIN, f'Updated by {message.from_user.id}: {message.from_user.full_name} {tup}')
                except:
                    await message.answer(f'Ошибка при изменения данных {tup=}')
                    await bot.send_message(ADMIN,f'Ошибка при изменения данных {tup=}')
            else:
                await message.answer(f"Komanda update sizga mumkin emas.")

    @routerUser.message(F.text.regexp(r"\d{4}-\d{2}-\d{2}"))  # Проверка формата даты YYYY-MM-DD
    async def date_handler(message: Message):
        await message.answer("Вы отправили дату!")

    return routerUser

# Переводим во float и всегда отрицательное число (расход)
def tofloat(z,idp):
    try:
        x = float(z)
        if idp !=ADMIN:
            x = -abs(x)
        return (True,x)
    except ValueError:
        return (False,z)
#-----------------------------------

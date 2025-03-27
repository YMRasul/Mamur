from aiogram import Router
from aiogram.types import Message
from keyboards import  main_kb
from aiogram.filters import Command
from config import ADMIN,DBASE
from datetime import datetime
from hendlers_user import tofloat
from dbase import DbaseBot

def get_routerEcho(bot):
    routerEcho = Router()

    @routerEcho.message(Command('help')) # Хэндлер на команду /help
    async def cmd_start(message: Message):
        s =     "'day YYYY-MM-DD' shu kun uchun hisobot\n"
        s = s + "'month YYYY-MM' bir oylik hisobot\n"
        s = s + "'rep YYYY-MM-DD' shu kundan boshlab hisobot\n"
        s = s + "'rpp YYYY-MM-DD YYYY-MM-DD' shu davr uchun hisobot\n"
        s = s + "'ins sum,datatime,text'  insert record\n"
        s = s + "'del IdRecord'  delete record\n"
        s = s + "'upd IdRecord,Text'  O'zgartirish\n"
        s = s + "/copy-получить БД\n"
        if message.from_user.id==ADMIN:
            s = s + "'set 139204666,6003890947, 1, 1'\n(set idadmin,iduser,vvod,report)\n"
            s = s + "'/sets' - Настройки"
        await message.answer(s + '\n/help',
                         reply_markup=main_kb(message.from_user.id))

    @routerEcho.message()
    async def Echo(message: Message):
        id = message.from_user.id
        name = message.from_user.full_name
        txt = message.text
        ms = [i.strip() for i in txt.split(',')]

        async with DbaseBot(DBASE) as db:
            s = "SELECT operid,vvod FROM users WHERE telegid = ?"
            cur = await db.fetch_one(s, (id,))  # Получаем настройки для id
            idp = cur[0]

        if len(ms) > 3:
            dt = ms[0] +' '+ ms[1]
            e1 = is_valid_datetime(dt)
            e2 = tofloat(ms[2],id)
            if (e1 and e2[0]):
                lis = [dt,e2[1],ms[3]]
                #lis = [DateTime,Smm,Text]
                idp = await insert(lis,message)
                #print(f'{idp=}')
            else:
                await message.reply(f'ID: {id} Text: {txt}')
                await bot.send_message(ADMIN, f'ID: {id} Text: {txt}')
        else:
            if id==ADMIN:
                await bot.send_message(idp, f'from admin:\n{txt}')
                await message.answer(f'{txt}\npassed to {idp}')

            else:
                await bot.send_message(ADMIN, f'from {id}:{name}\n{txt}')
                await message.answer(f'{txt}\npassed to Admin')

#
    async def insert(lis,message):
        id = message.from_user.id
        async with DbaseBot(DBASE) as db:
            s = "SELECT operid,vvod FROM users WHERE telegid = ?"
            cur = await db.fetch_one(s, (id,))  # Получаем настройки для id
            if cur[1] == 1:  # Если имеет право на ввод данных cur[0]
                #lis = [DateTime,Smm,Text,id]
                #rasxid, smm, datarecord, prim, iduser
                tup = (cur[0],lis[1],lis[0],lis[2],id)
                s = "INSERT INTO record (rasxid,smm,datarecord,prim,iduser) VALUES (?,?,?,?,?)"
                await db.execute(s, tup)

                if tup[1] < 0:
                    sd = f'Rashod:  {tup[1]} {tup[2]} {tup[3]}'
                else:
                    sd = f'Popolnenie:  {tup[1]} {tup[2]} {tup[3]}'
                await message.answer(sd)
                if id == ADMIN:
                    await bot.send_message(cur[0], sd)
                    await bot.send_message(cur[0], f'Inserted by {id}: {message.from_user.full_name}')
                else:
                    await bot.send_message(ADMIN, sd)
                    await bot.send_message(ADMIN, f'Inserted by {id}: {message.from_user.full_name}')
            else:
                await message.answer(f"Komanda ins sizga mumkin emas.")

    return routerEcho
    # 7554643826 Ma'murbek started

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
def is_valid_datetime(dt_str):
    try:
        datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False


'''            
                if id == ADMIN:
                    await bot.send_message(cur[0], sd)
                    await bot.send_message(cur[0], f'Inserted by {message.from_user.id}: {message.from_user.full_name}')
                else:
                    await bot.send_message(ADMIN, sd)
                    await bot.send_message(ADMIN, f'Inserted by {message.from_user.id}: {message.from_user.full_name}')
            else:
                await message.answer(f' {x[1]} строка не может быть преобразована во float')
'''

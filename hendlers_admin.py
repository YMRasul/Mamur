from aiogram import Router,F
from aiogram.types import Message
from config import ADMIN,DBASE
from aiogram.filters import Command

from dbase import DbaseBot

routerAdmin = Router()

# ------------------------------------------------
@routerAdmin.message((F.from_user.id==ADMIN)&(F.text[0:3]=='set'))
async def setts(message: Message):
    s = message.text[4:].strip()
    ms = [i.strip() for i in s.split(',')]
#    tup = (ms[1],ms[2],ms[3],ms[0])
    #set 139204666,6003890947, 7, 8
    try:
        idadm  = int(ms[0])
        iduser = int(ms[1])
        vvod   = int(ms[2])
        report = int(ms[3])

        tup = (iduser,vvod,report,idadm,)
        if idadm==ADMIN:
            try:
                async with DbaseBot(DBASE) as db:
                    st = 'UPDATE users SET operid==?, vvod==?,report==? WHERE telegid==?'
                    await db.execute(st, tup)
                await message.answer(f'Успешное сохранения данных {tup=}')
            except:
                await message.answer(f'Ошибка при сохранение данных {tup=}')
        else:
            await message.answer(f'Это для {ADMIN}')
    except:
        await message.answer(f"Command error!\n'set ida,idu, vvd, rep'")
# ---------------------------------------------
# /sets
@routerAdmin.message(Command('sets'))
async def setts(message: Message):
    id = message.from_user.id
    if id==ADMIN:
        await message.answer(f'{message.text}')
        async with DbaseBot(DBASE) as db:
            ss = "SELECT *FROM users"
            cur = await db.fetch_all(ss)  # Получаем настройки
            st = ''
            for row in cur:
                st = st + f'{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}\n'
                print(row[0],row[1],row[2],row[3],row[4])
            await message.answer(st)
    else:
        await message.answer(f'Это для {ADMIN}')
# ---------------------------------------------
@routerAdmin.message(F.text=="⚙️ Админ панель")
async def AdminInsert(message: Message):
    s1 = 'DELETE  FROM record'
    s2 = 'INSERT  INTO record(rasxid,smm,datarecord,prim,iduser) VALUES ' \
        '(6003890947,   200000,"2025-01-25 13:00","Prihod",139204666),' \
        '(6003890947,-15000.24,"2025-01-25 14:00","Obed",6003890947),' \
        '(6003890947,-55000.45,"2025-01-26 13:00","Producta",6003890947),' \
        '(6003890947,-70000.56,"2025-01-27 18:00","Bozorlik",6003890947),' \
        '(6003890947,-59000.50,"2025-01-27 19:00","Ujin",6003890947),' \
        '(6003890947,   200000,"2025-01-28 13:00","Prihod2",139204666),' \
        '(6003890947,-15000.24,"2025-01-28 14:00","Obed2",6003890947),' \
        '(6003890947,-55000.45,"2025-01-28 13:00","Producta2",6003890947),' \
        '(6003890947,-70000.56,"2025-01-29 18:00","Bozorlik2",6003890947),' \
        '(6003890947,-59000.50,"2025-01-29 19:00","Ujin2",6003890947),'\
        '(6003890947,   200000,"2025-02-01 13:00","Prihod3",139204666),' \
        '(6003890947,-15000.24,"2025-02-01 14:00","Obed3",6003890947),' \
        '(6003890947,-55000.45,"2025-02-02 13:00","Producta3",6003890947),' \
        '(6003890947,-70000.56,"2025-02-03 18:00","Bozorlik3",6003890947),' \
        '(6003890947,-59000.50,"2025-02-03 19:00","Ujin3",6003890947),' \
        '(6003890947,   200000,"2025-02-04 13:00","Prihod4",139204666),' \
        '(6003890947,-15000.24,"2025-02-05 14:00","Obed4",6003890947),' \
        '(6003890947,-55000.45,"2025-02-06 13:00","Producta4",6003890947),' \
        '(6003890947,-70000.56,"2025-02-07 18:00","Bozorlik4",6003890947),' \
        '(6003890947,-59000.50,"2025-02-08 19:00","Ujin4",6003890947),'\
        '(6003890947,   200000,"2025-02-27 13:00","Prihod5",139204666),' \
        '(6003890947,-15000.24,"2025-02-27 14:00","Obed5",6003890947),' \
        '(6003890947,-55000.45,"2025-02-27 13:00","Producta5",6003890947),' \
        '(6003890947,-70000.56,"2025-02-27 18:00","Bozorlik5",6003890947),' \
        '(6003890947,-59000.50,"2025-02-27 19:00","Ujin5",6003890947),'\
        '(6003890947,   200000,"2025-03-27 13:00","Prihod5",139204666),' \
        '(6003890947,-15000.24,"2025-03-02 14:00","Obed5",6003890947),' \
        '(6003890947,-55000.45,"2025-03-02 13:00","Producta5",6003890947),' \
        '(6003890947,-70000.56,"2025-03-02 18:00","Bozorlik5",6003890947),' \
        '(6003890947,-59000.50,"2025-03-07 19:00","Ujin5",6003890947)'

    async with DbaseBot(DBASE) as db:
        await db.execute(s1)
        await message.answer(f'Deleted all records')
        await db.execute(s2)
        await message.answer(f'Inserted records')


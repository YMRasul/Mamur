from aiogram import Router,F
from aiogram.types import Message
from config import ADMIN,DBASE
from datetime import datetime,date,timedelta
from soob import CMD0,CMD1,CMD4
from dateutil.relativedelta import relativedelta  #pip install python-dateutil

from dbase import DbaseBot

routerReport = Router()

# ========================== His date ================================
@routerReport.message(F.text=="📚 ReportAll")
async def how_are_you(message: Message):
    id = message.from_user.id
    async with DbaseBot(DBASE) as db:
        s = "SELECT operid,vvod,report FROM users WHERE telegid = ?"
        cur = await db.fetch_one(s, (id,)) # Получаем настройки для id
        s0 = 'SELECT SUM(smm) FROM record'
        x = await db.fetch_one(s0)
        if cur[2]==1: # Если имеет право на отчетности для cur[0]
            if id==ADMIN:
                s1 = "SELECT * FROM record order by datarecord"
                rec = await db.fetch_all(s1)  # За весь период
            else:
                s1 = "SELECT * FROM record WHERE rasxid==? order by datarecord"
                rec = await db.fetch_all(s1,(id,)) # За весь период
            if rec:
                s ='Hisobot\n'
                for row in rec:
                    s = s + f'{row[0]:4.0f}: {row[3]} , {row[2]:10.2f} , {row[4]}\n'
                s = s + f'Qoldiq: {x[0]:.2f}'
                await message.answer(s)
            else:
                await message.answer(f"No records!")
        else:
            await message.answer(f"Bu punkt yopilgan!")
#

@routerReport.message(F.text=="📚 ReportDay")
async def RepTekDay(message: Message):
    year = datetime.today().year
    mont = datetime.today().month

    if mont<10:
        dt1 = f'{year}-0{mont}-01 00:00'
    else:
        dt1 = f'{year}-{mont}-01 00:00'

    today = datetime.today().strftime('%Y-%m-%d')
    dt2 = today + ' 23:59'
    await message.answer(f"Shu {date.today()} kun uchun")
    ms0 = dt1
    ms1 = dt2
    await rep(ms0,ms1,message)
#PreviousMonth
@routerReport.message(F.text=="📚 PreviousMonth")
async def how_are_you(message: Message):
    year = datetime.today().year
    mont = datetime.today().month
    mont = mont - 1

    if mont ==0:
        mont = 12
        year = year -1

    if mont < 10:
        m1 = f'{year}-0{mont}-01 00:00'
    else:
        m1 = f'{year}-{mont}-01 00:00'

    dt1 = datetime.strptime(m1, "%Y-%m-%d %H:%M")
    dt2 = dt1 + relativedelta(months=1)
    m2 = dt2.strftime('%Y-%m-%d') + ' 00:00'

    print(f'{m1=} {m2=}')

    await message.answer(f"O'tgan oy")
    await rep(m1,m2,message)

# ---------------------------------------------------
@routerReport.message(F.text=="📚 ReportMonth")
async def reptekmonth(message: Message):
    year = datetime.today().year
    mont = datetime.today().month

    if mont<10:
        tekmonth = f'{year}-0{mont}'
    else:
        tekmonth = f'{year}-{mont}'

    dt1 = tekmonth+'-01 00:00'

    today = datetime.today().strftime('%Y-%m-%d')
    dt2 = today + ' 23:59'

    await message.answer(f"Shu {tekmonth} oy uchun")
    ms0 = dt1
    ms1 = dt2
    await rep(ms0,ms1,message)
#==========================Rep ================================
# rep 2025-01-01    (Hisobot от даты = 2025-01-01)
@routerReport.message(F.text.lower().startswith("rep"))
async def Hisobot1(message: Message):
    id = message.from_user.id
    s = message.text[4:].strip()
    ms = [i.strip() for i in s.split(',')]
    if len(ms)==1:
        try:
            dt1 = datetime.strptime(ms[0],"%Y-%m-%d")
            m1 = dt1.strftime('%Y-%m-%d') + ' 00:00'

            today = datetime.today().strftime('%Y-%m-%d')
            dt2 = today + ' 23:59'
            #await message.answer(f'{dt1=} {dt2=}')
        except ValueError:
            await message.answer(f'Xato date: {ms[0]}')
            return
    else:
        await message.answer(f"Error!\nKomanda {CMD0} ko'rinishda bo'lishi kerak.")
        return

    await message.answer(f'Date: {m1}')
    ms0 = m1
    ms1 = dt2
    await rep(ms0,ms1,message)

# rpp 2025-01-01 09:15,2025-01-05 14:43   Hisobot за период
@routerReport.message(F.text.lower().startswith("rpp"))
async def Hisobot2(message: Message):
    id = message.from_user.id
    name = message.from_user.full_name
    s = message.text[4:].strip()
    ms = [i.strip() for i in s.split(',')]
    if len(ms)==2:
        try:
            dt1 = datetime.strptime(ms[0],"%Y-%m-%d")
            dt2 = datetime.strptime(ms[1],"%Y-%m-%d")
        except ValueError:
            await message.answer(f'Xato date: {ms[0]},{ms[1]}')
            return
    else:
        await message.answer(f"Error!\nKomanda {CMD1} ko'rinishda bo'lishi kerak.")
        return
    await message.answer(f'Date: {dt1} {dt2}')

    ms0 = ms[0]
    ms1 = ms[1]
    await rep(ms0,ms1,message)
# ======================================================================
async def rep(ms0,ms1,message):
    idp = message.from_user.id
    async with DbaseBot(DBASE) as db:
        s = "SELECT operid,vvod,report,fullname FROM users WHERE telegid = ?"
        cur = await db.fetch_one(s, (idp,)) # Получаем настройки для id
        idr = cur[0]
        nmp = cur[3]
        await message.answer(f'{nmp}')
        if cur[2]==1: # Если имеет право на отчетности для cur[0]
            x1 = 'SELECT SUM(smm) FROM record WHERE datarecord < ?'
            ost1 = await db.fetch_one(x1,(ms0,))
            os1 = 0 if ost1[0]==None else ost1[0]

            x2 = 'SELECT SUM(smm) FROM record WHERE datarecord <= ?'
            ost2 = await db.fetch_one(x2,(ms1,))
            os2 = 0 if ost2[0]==None else ost2[0]

            tp = (idr, ms0, ms1,)
            s1 = "SELECT * FROM record WHERE (rasxid==? and datarecord >= ? and datarecord <= ? )" \
                 " order by datarecord"
            rec = await db.fetch_all(s1, tp)  # За  период

            s2 = "SELECT SUM(smm) FROM record WHERE" \
                 " (rasxid==? and datarecord >= ? and datarecord <= ?  and smm > 0)" \
                 " order by datarecord"
            pri = await db.fetch_one(s2, tp) # Приход
            prx = 0 if pri[0]==None else pri[0]

            s3 = "SELECT SUM(smm) FROM record WHERE" \
                 " (rasxid==? and datarecord >= ? and datarecord <= ?  and smm < 0)" \
                 " order by datarecord"
            ras = await db.fetch_one(s3, tp) # Приход
            rsx = 0 if ras[0]==None else ras[0]

#            print(s2,pri[0])
#            print(s3,ras[0])

            if rec:

                s = f'Qoldiq: {os1:.2f}\n'
                for row in rec:
                    s = s + f'{row[0]:4.0f}:{row[3]},{row[2]:10.2f},{row[4]}\n'

                s = s + f'Prihod: {prx:.2f}\n'
                s = s + f'Rashod: {rsx:.2f}\n'
                s = s + f'Qoldiq: {os2:.2f}'

                await message.answer('<code>' + s + '</code>')
            else:
                await message.answer(f"No records!")
        else:
            await message.answer(f"Bu punkt yopilgan!")
#---------------------------------------------------
# month 2025-02   Hisobot за месяц
@routerReport.message(F.text.lower().startswith("month"))  # Hisobot за месяц
async def Hisobotm(message: Message):
    s = message.text[6:].strip()
    ms = [i.strip() for i in s.split(',')]
    if len(ms)==1:
        try:
            m1 = ms[0]+'-01 00:00'
            dt1 = datetime.strptime(m1,"%Y-%m-%d %H:%M")

            dt2 = dt1 + relativedelta(months=1)
            m2 = dt2.strftime('%Y-%m-%d') + ' 00:00'
        except ValueError:
            await message.answer(f'Xato date: {ms[0]}')
            return
    else:
        await message.answer(f"Error!\nKomanda {CMD4} ko'rinishda bo'lishi kerak.")
        return

    ms0 = m1
    ms1 = m2
    await rep(ms0,ms1,message)
# --------------------------------------------------
# day 2025-02-01   Hisobot за день
@routerReport.message(F.text.lower().startswith("day"))  # Hisobot за месяц
async def Hisobotd(message: Message):
    id = message.from_user.id
    s = message.text[4:].strip()
    ms = [i.strip() for i in s.split(',')]

    if len(ms) == 1:
        try:
            dt1 = datetime.strptime(ms[0], "%Y-%m-%d")
            m1 = dt1.strftime('%Y-%m-%d') + ' 00:00'
            m2 = dt1.strftime('%Y-%m-%d') + ' 23:59'
            await message.answer(f'For  {ms[0]}')
        except ValueError:
            await message.answer(f'Xato date: {ms[0]}')
            return
    else:
        await message.answer(f"Error!\nKomanda {CMD3} ko'rinishda bo'lishi kerak.")
        return
    await rep(m1,m2,message)

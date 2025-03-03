from aiogram import Router
from aiogram.types import Message
from keyboards import  main_kb
from aiogram.filters import Command
from config import ADMIN

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
        if message.from_user.id==ADMIN:
            s = s + "'set 139204666,6003890947, 1, 1'\n(set idadmin,iduser,vvod,report)\n"
            s = s + "'/sets' - Настройки"
        await message.answer(s + '\n/help',
                         reply_markup=main_kb(message.from_user.id))

    @routerEcho.message()
    async def Echo(message: Message):
        await message.reply(f'ID: {message.from_user.id} Text: {message.text}')
        await bot.send_message(ADMIN, f'ID: {message.from_user.id} Text: {message.text}')

    return routerEcho
    # 7554643826 Ma'murbek started
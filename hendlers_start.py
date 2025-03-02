from aiogram import F, Router  # F - это magic фильтр
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dbase import DbaseBot
from config import DBASE,ADMIN
from keyboards import main_kb

def get_router(bot):
    routerStart = Router()

    #routerStart = Router()

    @routerStart.message(CommandStart()) # Хэндлер на команду /start
    async def cmd_start(message: Message):
        async with DbaseBot(DBASE) as dbs:
            if not await dbs.check_user(message.from_user.id):
                await dbs.add_user(message.from_user.id,message.from_user.full_name,message.from_user.id,)
        await message.reply(f'Salom.\nID raqamingiz: {message.from_user.id}\n'
                        f'Ismingiz: {message.from_user.full_name}',reply_markup=main_kb(message.from_user.id))
        await bot.send_message(ADMIN, f'{message.from_user.id} {message.from_user.full_name} started')


    @routerStart.message(F.photo)
    async def get_photo(message: Message):
        await message.answer(f'ID фото: {message.photo[-1].file_id}')


    @routerStart.message(Command('get_photo'))
    async def get_photo(message: Message):
        await message.answer_photo(photo=
                               'AgACAgIAAxkBAANkZ7MGaVSNT3RtHnpULbIJVXuq9CAAAvvpMRsZ6phJjmZG6F0xlqoBAAMCAAN4AAM2BA',
                               caption='Жасурбек')

    return routerStart
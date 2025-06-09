from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from sqlalchemy import select

from storage.database import async_session, User
from locales.translator import translate

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user_lang = message.from_user.language_code or "ru"

    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            user = User(tg_id=user_id, language=user_lang)
            session.add(user)
            await session.commit()

    text = translate("welcome", message.from_user.language_code)
    await message.answer(text)


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    text = translate("help", message.from_user.language_code)
    await message.answer(text)
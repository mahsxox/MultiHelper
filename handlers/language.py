from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.language_kb import get_language_keyboard
from storage.database import async_session, User

router = Router()

@router.message(F.text == "/language")
async def choose_language(message: Message, state: FSMContext):
    await message.answer(
        "Выберите язык / Choose your language:",
        reply_markup=get_language_keyboard()
    )

@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: CallbackQuery):
    lang_code = callback.data.split("_")[1]
    tg_id = callback.from_user.id

    async with async_session() as session:
        result = await session.execute(
            User.__table__.update().where(User.tg_id == tg_id).values(language=lang_code)
        )
        await session.commit()

    await callback.message.edit_text(
        "✅ Язык изменён!" if lang_code == "ru" else "✅ Language updated!"
    )
    await callback.answer()
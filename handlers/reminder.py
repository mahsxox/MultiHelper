from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from datetime import datetime
from sqlalchemy import select
from storage.database import async_session, User, Reminder
from states.reminder_state import RemindStates
from locales.translator import translate

router = Router()

@router.message(F.text == "/remind")
async def cmd_remind(message: Message, state: FSMContext):
    await state.set_state(RemindStates.waiting_text)
    await message.answer(translate("enter_reminder_text", message.from_user.language_code))


@router.message(RemindStates.waiting_text)
async def handle_reminder_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(RemindStates.waiting_datetime)
    await message.answer(translate("enter_reminder_time", message.from_user.language_code))


@router.message(RemindStates.waiting_datetime)
async def handle_reminder_time(message: Message, state: FSMContext):
    user_input = message.text.strip()
    try:
        remind_time = datetime.strptime(user_input, "%d.%m.%Y %H:%M")
    except ValueError:
        await message.answer(translate("invalid_time", message.from_user.language_code))
        return

    data = await state.get_data()
    await state.clear()

    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.tg_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        if not user:
            await message.answer("❗ Пользователь не найден в базе данных.")
            return

        reminder = Reminder(
            user_id=user.id,
            text=data["text"],
            remind_at=remind_time
        )
        session.add(reminder)
        await session.commit()

    await message.answer(translate("reminder_saved", message.from_user.language_code))
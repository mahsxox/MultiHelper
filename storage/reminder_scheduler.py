import asyncio
from datetime import datetime
from aiogram import Bot
from sqlalchemy import select
from storage.database import async_session, Reminder
from sqlalchemy.orm import joinedload

CHECK_INTERVAL = 60

async def check_reminders(bot: Bot):
    while True:
        async with async_session() as session:
            now = datetime.now()
            result = await session.execute(
                select(Reminder).options(joinedload(Reminder.user)).where(Reminder.remind_at <= now)
            )
            reminders = result.scalars().all()

            for reminder in reminders:
                try:
                    print(f'reminder_user: {reminder.user}')
                    await bot.send_message(reminder.user.tg_id, f"🔔 Напоминание: {reminder.text}")
                except Exception as e:
                    print(f"[!] Не удалось отправить напоминание: {e}")

                await session.delete(reminder)

            await session.commit()
        await asyncio.sleep(CHECK_INTERVAL)
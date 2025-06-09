from aiogram import Router, F
from aiogram.types import Message
from services.motivation import get_random_quote

router = Router()

@router.message(F.text == "/motivation")
async def cmd_motivation(message: Message):
    quote, author = get_random_quote()
    await message.answer(f'💡"{quote}" \n\n— {author}')
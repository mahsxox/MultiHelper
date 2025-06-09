from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Awaitable, Dict, Any

from services.gas_logger import log_to_google

class OuterLoggerMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], message: Message, data: Dict[str, Any]) -> Any:
        log_to_google(message.from_user.id, message.text)
        return await handler(message, data)
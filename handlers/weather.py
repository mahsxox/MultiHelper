from aiogram import Router, types, F
from aiogram.filters import Command
from services.weather import get_weather
from keyboards.weather_kb import get_weather_keyboard
from locales.translator import translate

router = Router()

@router.message(Command("weather"))
async def weather_choose(message: types.Message):
    lang = message.from_user.language_code or "ru"
    keyboard = get_weather_keyboard(lang)
    await message.answer(translate("choose_city", lang), reply_markup=keyboard)

@router.callback_query(F.data.startswith("weather:"))
async def weather_result(callback: types.CallbackQuery):
    city_key = callback.data.split(":")[1]
    lang = callback.from_user.language_code or "ru"
    weather_text = await get_weather(city_key, lang)
    await callback.message.answer(weather_text)
    await callback.answer()
from aiogram.utils.keyboard import InlineKeyboardBuilder
from locales.translator import translate

def get_weather_keyboard(lang: str):
    kb = InlineKeyboardBuilder()
    kb.button(text=translate("city_moscow", lang), callback_data="weather:moscow")
    kb.button(text=translate("city_spb", lang), callback_data="weather:spb")
    return kb.as_markup()
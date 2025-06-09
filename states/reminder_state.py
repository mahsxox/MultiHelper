from aiogram.fsm.state import StatesGroup, State

class RemindStates(StatesGroup):
    waiting_text = State()
    waiting_datetime = State()
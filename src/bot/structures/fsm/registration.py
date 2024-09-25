from aiogram.fsm.state import StatesGroup, State


class RegisterGroup(StatesGroup):
    """Use this state for registration"""
    
    fullname = State()
    age = State()
    phone_number = State()

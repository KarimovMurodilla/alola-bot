from aiogram.fsm.state import StatesGroup, State


class RegisterGroup(StatesGroup):
    """Use this state for registration"""
    
    phone_number = State()

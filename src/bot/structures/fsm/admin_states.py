from aiogram.fsm.state import StatesGroup, State


class AdminStatesGroup(StatesGroup):
    """Use this state for registration"""
    
    broadcast = State()

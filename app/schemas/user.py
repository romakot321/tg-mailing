from aiogram.fsm.state import State, StatesGroup


class UserRegisterForm(StatesGroup):
    input_age = State()
    input_gender = State()

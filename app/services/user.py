from aiogram.types import CallbackQuery, Message
from typing import Annotated
from loguru import logger
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram3_di import Depends

from app.schemas.user import UserRegisterForm
from app.repositories.user import UserRepository
from db.tables import User


def make_row_keyboard(*items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)



class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    @classmethod
    def init(
            cls,
            user_repository: Annotated[
                UserRepository, Depends(UserRepository.init)],
    ):
        return cls(user_repository)

    async def handle_start_register(self, message: Message, context: FSMContext):
        await message.answer(text="Введите ваш возраст")
        await context.set_state(UserRegisterForm.input_age)

    async def handle_register_age_input(self, message: Message, context: FSMContext):
        await context.update_data(age=int(message.text))
        await message.answer(text="Введите ваш пол", reply_markup=make_row_keyboard("Мужской", "Женский"))
        await context.set_state(UserRegisterForm.input_gender)

    async def handle_register_gender_input(self, message: Message, context: FSMContext):
        register_form = await context.get_data()
        register_form.update({'gender': message.text.lower()})
        model = User(id=message.from_user.id, **register_form)
        logger.debug(await self.user_repository.create(model))

        await message.answer(
            "Вы успешно зарегестрированы.",
            reply_markup=ReplyKeyboardRemove()
        )
        await context.clear()


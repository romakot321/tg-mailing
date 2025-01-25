from typing import Annotated

from aiogram import F
from aiogram import Router, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram3_di import Depends
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.services.user import UserService
from app.schemas.action import ActionCallback
from app.schemas.user import UserRegisterForm

router = Router(name=__name__)


@router.message(StateFilter(None), CommandStart())
async def register_start_command(
        message: Message,
        state: FSMContext,
        service: Annotated[
            UserService, Depends(UserService.init)],
):
    return await service.handle_start_register(message, state)


@router.message(UserRegisterForm.input_age, F.text.isdigit())
async def register_age_input(
        message: Message,
        state: FSMContext,
        service: Annotated[
            UserService, Depends(UserService.init)],
):
    return await service.handle_register_age_input(message, state)


@router.message(UserRegisterForm.input_age)
async def register_age_input_invalid(message: Message):
    await message.answer("Неверный ввод, пожалуйста введите ваш возраст")


@router.message(UserRegisterForm.input_gender, F.text.in_(["Мужской", "Женский"]))
async def register_gender_input(
        message: Message,
        state: FSMContext,
        service: Annotated[
            UserService, Depends(UserService.init)],
):
    return await service.handle_register_gender_input(message, state)


@router.message(UserRegisterForm.input_gender)
async def register_age_input_invalid(message: Message):
    await message.answer("Неверный ввод, пожалуйста выберите ваш пол из списка ниже")


#@router.callback_query(
#    ActionCallback.filter(
#        F.action == Action.start.action_name
#    )
#)
#async def start_callback(
#        query: CallbackQuery,
#        callback_data: ActionCallback,
#        bot: Bot,
#        service: Annotated[
#            UserService, Depends(UserService.init)]
#):
#    method = await service.handle_user_choose(
#        query.from_user.id,
#        query.message.message_id,
#        Action.start,
#        is_startped=False
#    )
#    return await bot(method)


#@router.callback_query(
#    UserActionCallback.filter(
#        F.action == Action.start.action_name
#    )
#)
#async def start_callback_with_user(
#        query: CallbackQuery,
#        callback_data: UserActionCallback,
#        bot: Bot,
#        service: Annotated[
#            UserService, Depends(UserService.init)]
#):
#    telegram_id = query.from_user.id
#    user_id = callback_data.user_id
#    method = await service.handle_start_callback(
#        telegram_id,
#        query.message.message_id,
#        user_id
#    )
#    return await bot(method)

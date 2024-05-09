from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards import (
    start,
    stop,
)


router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await message.answer(
        text=start.greating
    )
    await message.answer(
        text=start.agreement,
        reply_markup=start.get_keyboard()
    )
    await state.set_state(None)


@router.message(Command("stop"))
async def stop_handler(message: Message, state: FSMContext):
    await message.answer(
        text=stop.goodbye,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(None)
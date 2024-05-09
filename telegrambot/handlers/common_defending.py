from aiogram import Router
from aiogram.types import Message

from keyboards import (
    last_frontier
)


router = Router()


@router.message()
async def last_frontier_handler(message: Message):
    await message.answer(
        text=last_frontier.text
    )
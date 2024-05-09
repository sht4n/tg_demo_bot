from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from filters.admin import Verification


ADMINS=(
    538855523,
)

router = Router()
router.message.filter(
    Verification(admin_ids=ADMINS)
)


@router.message(Command("admin"))
async def admin_handler(msg: Message):
    await msg.answer(
        "admin mode is <b>on</b>",
        reply_markup=ReplyKeyboardRemove()
    )


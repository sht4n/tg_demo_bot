from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from keyboards import (
    end_question,
    feed_form,
    match_form,
)

from db import load_form, update_like, get_match


router = Router()


class Feed(StatesGroup):
    form = None
    last_user_id = None
    go=State()


# first form in feed
@router.message(
    Feed.go, 
    F.text.in_(end_question.options[0])
)
async def start_handler(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    first_form = load_form(source_user_id=user_id)
    await message.answer(
        text=feed_form.text,
        reply_markup=feed_form.get_keyboard()
    )
    await state.update_data(last_user_id=first_form["user_id"])
    await message.answer_media_group(
        media=feed_form.form_builder(form=first_form)
    )
    form = load_form(source_user_id=user_id)
    await state.update_data(form=form)

# all form in feed
@router.message(
    Feed.go,
    F.text.in_(feed_form.options)
)
async def base_handler(message: Message, state: FSMContext):
    source_user_id = str(message.from_user.id)
    user_data = await state.get_data()
    target_user_id = user_data["last_user_id"]
    is_like = feed_form.options[1] == message.text
    update_like(
        source_user_id=source_user_id,
        target_user_id=target_user_id,
        is_like=is_like,
    )
    match = get_match(source_user_id=source_user_id) 
    if match is not None: # matches
        form = user_data["form"]
        await message.answer(
            text=match_form.text,
            reply_markup=match_form.get_keyboard()
        )
        await state.update_data(last_user_id=form["user_id"])
        await message.answer_media_group(
            media=feed_form.form_builder(form=form)
        )
    elif match is None: # no matches
        form = user_data["form"]
        await state.update_data(last_user_id=form["user_id"])
        await message.answer_media_group(
            media=feed_form.form_builder(form=form)
        )
        form = load_form(source_user_id=source_user_id)
        await state.update_data(form=form)

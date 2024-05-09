import io

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards import (
    start_question,
    geo_question,
    goal_question,
    gender_question,
    preference_question,
    name_question,
    incorrect_name_question,
    age_question,
    incorrect_age_question,
    description_question,
    photo_question,
    uploading_photo,
    final_form,
    end_question
)

from db import dump_form
from .common import start
from .feeding import Feed
from .utls import get_city


router = Router()


class Questionnaire(StatesGroup):
    user_id = None
    start = State()
    geo = State()
    goal = State()
    gender = State()
    preference = State()
    name = State()
    age = State()
    description = State()
    uploading_photo = State()
    first_photo = State()
    second_photo = State()
    third_photo = State()
    final_form = State()


# start question
@router.message(
    StateFilter(None), 
    F.text.in_(start.options)
)
async def start_handler(message: Message, state: FSMContext):
    await message.answer(
        text=start_question.text,
        reply_markup=start_question.get_keyboard()
    )
    await state.set_state(Questionnaire.start)


# geo question
@router.message(
    Questionnaire.start
)
async def start_handler(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    await state.update_data(user_id=user_id)
    await message.answer(
        text=geo_question.text,
        reply_markup=geo_question.get_keyboard()
    )
    await state.set_state(Questionnaire.geo)


# goal question
@router.message(
    Questionnaire.geo,    
    F.location
)
async def goal_handler(message: Message, state: FSMContext):
    lat, long = (
        message.location.latitude,
        message.location.longitude
    )
    await state.update_data(geo=(lat, long))
    await state.update_data(city=get_city(lat, long))
    await message.answer(
        text=goal_question.text,
        reply_markup=goal_question.get_keyboard()
    )
    await state.set_state(Questionnaire.goal)


# gender question
@router.message(
    Questionnaire.goal, 
    F.text.in_(goal_question.options)
)
async def gender_handler(message: Message, state: FSMContext):
    if message.text == goal_question.options[0]:
        goal = "networking"
    elif message.text == goal_question.options[1]:
        goal = "partner"
    else:
        goal = None
    await state.update_data(goal=goal)
    await message.answer(
        text=gender_question.text,
        reply_markup=gender_question.get_keyboard()
    )
    await state.set_state(Questionnaire.gender)


# preference question
@router.message(
    Questionnaire.gender,
    F.text.in_(gender_question.options)
)
async def preference_handler(message: Message, state: FSMContext):
    if message.text == gender_question.options[0]:
        gender = "female"
    elif message.text == gender_question.options[1]:
        gender = "male"
    elif message.text == gender_question.options[2]:
        gender = "non-binary"
    else:
        gender = None
    await state.update_data(gender=gender)
    await message.answer(
        text=preference_question.text,
        reply_markup=preference_question.get_keyboard()
    )
    await state.set_state(Questionnaire.preference)


# name question
@router.message(
    Questionnaire.preference,
    F.text.in_(preference_question.options)
)
async def name_handler(message: Message, state: FSMContext):
    if message.text == preference_question.options[0]:
        preference = "female"
    elif message.text == preference_question.options[1]:
        preference = "male"
    elif message.text == preference_question.options[2]:
        preference = "all"
    else:
        preference = None
    await state.update_data(preference=preference)
    await message.answer(
        text=name_question.text,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Questionnaire.name)


# age question (if name is correct)
@router.message(
    Questionnaire.name,
    F.text.regexp(r'^[a-zA-Zа-яА-Я]+$')
)
async def age_handler(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        text=age_question.text,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Questionnaire.age)


# if name is incorrect
@router.message(
    Questionnaire.name,
)
async def age_handler(message: Message, state: FSMContext):
    await message.answer(
        text=incorrect_name_question.text,
        reply_markup=ReplyKeyboardRemove()
    )


# description question (if age is correct)
@router.message(
    Questionnaire.age,
    F.text.isdigit(),
    F.text.func(lambda text: 11 < int(text) < 100)
)
async def description_handler(message: Message, state: FSMContext):
    age = int(message.text)
    await state.update_data(age=age)
    await message.answer(
        text=description_question.text,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Questionnaire.description)


# if age is incorrect
@router.message(
    Questionnaire.age
)
async def incorrect_age_handler(message: Message, state: FSMContext):
    await message.answer(
        text=incorrect_age_question.text,
        reply_markup=ReplyKeyboardRemove()
    )


# photo question
@router.message(
    Questionnaire.description,
    F.text
)
async def photo_handler(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(
        text=photo_question.text,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Questionnaire.uploading_photo)


# first photo
@router.message(
    Questionnaire.uploading_photo,
    F.photo
)
async def first_photo_handler(message: Message, state: FSMContext):
    photo = io.BytesIO()
    photo_id = message.photo[-1].file_id
    await message.bot.download(file=photo_id, destination=photo)
    await state.update_data(first_photo={
            "first_photo_id": photo_id,
            "first_photo": photo.getvalue(),
        }
    )
    await message.answer(
        text=uploading_photo.text,
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text=uploading_photo.first,
        reply_markup=uploading_photo.get_keyboard()
    )
    await state.set_state(Questionnaire.first_photo)


# second photo
@router.message(
    Questionnaire.first_photo,
    F.photo
)
async def second_photo_handler(message: Message, state: FSMContext):
    photo = io.BytesIO()
    photo_id = message.photo[-1].file_id
    await message.bot.download(file=photo_id, destination=photo)
    await state.update_data(second_photo={
            "second_photo_id": photo_id,
            "second_photo": photo.getvalue(),
        }
    )
    await message.answer(
        text=uploading_photo.text,
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text=uploading_photo.second,
        reply_markup=uploading_photo.get_keyboard()
    )
    await state.set_state(Questionnaire.second_photo)


# third photo
@router.message(
    Questionnaire.second_photo,
    F.photo
)
async def third_photo_handler(message: Message, state: FSMContext):
    photo = io.BytesIO()
    photo_id = message.photo[-1].file_id
    await message.bot.download(file=photo_id, destination=photo)
    await state.update_data(third_photo={
            "third_photo_id": photo_id,
            "third_photo": photo.getvalue(),
        }
    )
    await message.answer(
        text=uploading_photo.text,
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text=uploading_photo.third,
        reply_markup=uploading_photo.get_keyboard()
    )
    await state.set_state(Questionnaire.third_photo)


# if fourth photo
@router.message(
    Questionnaire.third_photo,
    F.photo
)
async def fourth_photo_handler(message: Message, state: FSMContext):
    await message.answer(
        text=uploading_photo.fourth,
        reply_markup=uploading_photo.get_keyboard()
    )
    await state.set_state(Questionnaire.third_photo)


# final form
@router.message(
    F.text.in_(uploading_photo.options)
)
async def form_handler(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer_media_group(
        media=final_form.form_builder(user_data=user_data)
    )
    await message.answer(
        text=final_form.text,
        reply_markup=final_form.get_keyboard()
    )
    await state.set_state(Questionnaire.final_form)


# if restart
@router.message(
    F.text == final_form.options[1]
)
async def start_handler(message: Message, state: FSMContext):
    await message.answer(
        text=start_question.text,
        reply_markup=start_question.get_keyboard()
    )
    await state.set_state(Questionnaire.start)


# end form
@router.message(
    F.text == final_form.options[0]
)
async def end_handler(message: Message, state: FSMContext):
    user_data = await state.get_data()
    dump_form(user_data=user_data)
    await message.answer(
        text=end_question.text,
        reply_markup=end_question.get_keyboard()
    )
    await state.set_state(Feed.go)

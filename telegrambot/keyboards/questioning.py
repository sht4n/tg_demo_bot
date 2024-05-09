from aiogram import types
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from typing import Any, Dict, List

from .utls import get_years_old


class Question():
    def __init__(self, text: str) -> None:
        self.text = text


class ClosedQuestion(Question):
    def __init__(self, text: str, options: List[str]) -> None:
        super().__init__(text)
        self.options = options

    def get_keyboard(self) -> types.ReplyKeyboardMarkup:
        reply_builder = ReplyKeyboardBuilder()
        for option in self.options:
            reply_builder.add(
                types.KeyboardButton(
                    text=option
                )
            )
        return reply_builder.as_markup(resize_keyboard=True)


class GeoQuestion(Question):
    def __init__(self, text: str, options: List[str]) -> None:
        super().__init__(text)
        self.options = options
    
    def get_keyboard(self) -> types.ReplyKeyboardMarkup:
        reply_builder = ReplyKeyboardBuilder()
        for option in self.options:
            reply_builder.add(
                types.KeyboardButton(
                    text=option,
                    request_location=True
                )
            )
        return reply_builder.as_markup(resize_keyboard=True)


class UploadingPhoto(ClosedQuestion):
    def __init__(
        self,
        text: str,
        first: str,
        second: str,
        third: str,
        fourth: str,
        options: List[str]
    ) -> None:
        super().__init__(text, options)
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth


class FinalForm(ClosedQuestion):
    def __init__(self, text: str, options: List[str]) -> None:
        super().__init__(text, options)

    def form_builder(self, user_data: Dict[str, Any]) -> List[types.InputMediaPhoto]:
        city = user_data["city"]
        name = user_data["name"]
        age = user_data["age"]
        years_old = get_years_old(age)
        description = user_data["description"]
        album_builder = MediaGroupBuilder(
            caption=f"{name}, {age} {years_old}, {city}\n{description}"
        )
        if "first_photo" in user_data:
            album_builder.add_photo(
                media=user_data["first_photo"]["first_photo_id"]
            )
        if "second_photo" in user_data:
            album_builder.add_photo(
                media=user_data["second_photo"]["second_photo_id"]
            )
        if "third_photo" in user_data:
            album_builder.add_photo(
                media=user_data["third_photo"]["third_photo_id"]
            )
        return album_builder.build()

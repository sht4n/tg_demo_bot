from aiogram import types
from aiogram.utils.media_group import MediaGroupBuilder
from typing import List

from db import Form
from .questioning import ClosedQuestion
from .utls import get_years_old


class FeedForm(ClosedQuestion):
    def __init__(self, text: str, options: List[str]) -> None:
        super().__init__(text, options)

    def form_builder(self, form: Form) -> List[types.InputMediaPhoto]:
        city = form["city"]
        name = form["name"]
        age = form["age"]
        years_old = get_years_old(age)
        description = form["description"]
        album_builder = MediaGroupBuilder(
            caption=f"{name}, {age} {years_old}, {city}\n{description}"
        )
        if form.get("first_photo_id") is not None:
            album_builder.add_photo(
                media=form["first_photo_id"]
            )
        if form.get("second_photo_id") is not None:
            album_builder.add_photo(
                media=form["second_photo_id"]
            )
        if form.get("third_photo_id") is not None:
            album_builder.add_photo(
                media=form["third_photo_id"]
            )
        return album_builder.build()
    
class MatchForm(FeedForm):
    def __init__(self, text: str, options: List[str]) -> None:
        super().__init__(text, options)

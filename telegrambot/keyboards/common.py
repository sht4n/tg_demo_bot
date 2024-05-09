from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class Start():
    def __init__(self, greating, agreement, options) -> None:
        self.greating = greating
        self.agreement = agreement
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


class Stop():
    def __init__(self, goodbye) -> None:
        self.goodbye = goodbye


class LastFrontier():
    def __init__(self, text) -> None:
        self.text = text

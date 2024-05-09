from .common import *
from .questioning import *
from .feeding import *


start = Start(
    greating = "Привет! Это бот для поиска знакомств",
    agreement = "Продолжая, ты подтверждаешь согласие с пользовательским соглашением и правилами конфиденциальности",
    options = (
        "оки",
    )
)

stop = Stop(
    goodbye="Хорошо! Приходи позже"
)

last_frontier = LastFrontier(
    text="Я не понял, что ты имеешь в виду ((\nПопробуй пожалуйста еще раз"
)

start_question = ClosedQuestion(
    text = "Отлично! Давай начнем заполнять твою анкету?",
    options = (
        "давай заполним!",
    )
)

geo_question = GeoQuestion(
    text = "Поделитесь пожалуйста геолокацией",
    options = (
        "отправить геолокацию",
    )
)

goal_question = ClosedQuestion(
    text = "Кого ты хочешь найти?",
    options = (
        "знакомства/друзей",
        "партнера"
    )
)

gender_question = ClosedQuestion(
    text = "Теперь выбери пол",
    options = (
        "я девушка",
        "я парень",
        "не хочу выбирать"
    )
)

preference_question = ClosedQuestion(
    text = "Кто тебе интересен?",
    options = (
        "девушки",
        "парни",
        "все"
    )
)

name_question = Question(text="Как тебя зовут?")
incorrect_name_question = Question(text="Некорректное имя. Используй пожалуйста только буквы без пробелов")
age_question = Question(text="Сколько тебе лет?")
incorrect_age_question = Question(text="Некорректный возраст. Используй пожалуйста только цифры без пробелов")
description_question = Question(text="Напиши описание своей анкеты")
photo_question = Question(text="Приложи 1 фото к своей анкете")

uploading_photo = UploadingPhoto(
    text = "Поймал твое фото!",
    first = "Ты приложил 1/3 фото. Можешь загрузить еще фото или закончить оформление анкеты",
    second = "Ты приложил 2/3 фото. Можешь загрузить еще фото или закончить оформление анкеты",
    third = "Ты приложил 3/3 фото. Пора закончить оформление анкеты",
    fourth = "Ты уже приложил 3/3 фото. Пора закончить оформление анкеты",
    options = (
        "закончить",
    )
)

final_form = FinalForm(
    text = "Вот твоя итоговая анкета",
    options = (
        "отлично!",
        "заполнить заново"
    )
)

end_question = ClosedQuestion(
    text = "Начнем поиск знакомств!",
    options = (
        "го!",
    )
)

feed_form = FeedForm(
    text = "поиск...",
    options = (
        "нет",
        "да"
    )
)

match_form = MatchForm(
    text = "Новый мэтч!",
    options = (
        "нет",
        "да",
    )
)

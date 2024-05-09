FROM python:3.12

COPY bot.py config_reader.py db.py requirements.txt /telegrambot/
COPY /filters/ /telegrambot/filters/
COPY /handlers/ /telegrambot/handlers/
COPY /keyboards/ /telegrambot/keyboards/

WORKDIR /telegrambot

RUN pip install -r requirements.txt

CMD ["python", "bot.py"]

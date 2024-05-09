FROM python:3.12


COPY requirements.txt /recsys/
COPY . /recsys/

WORKDIR /recsys

RUN pip install -r requirements.txt

CMD ["python", "main.py"]

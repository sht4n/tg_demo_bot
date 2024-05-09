FROM python:3.12

COPY requirements.txt /dbapi/
COPY . /dbapi/

WORKDIR /dbapi

RUN pip install -r requirements.txt

CMD ["python", "main.py"]

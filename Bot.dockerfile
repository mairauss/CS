FROM python:3.7

ADD requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY ./src /app/src

WORKDIR /app/src

CMD ["python", "main.py"]
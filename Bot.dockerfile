FROM python:3.7

ADD requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY . /app/

WORKDIR /app

CMD ["python", "main.py"]
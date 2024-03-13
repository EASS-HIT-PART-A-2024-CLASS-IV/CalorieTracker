FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8000

ENV REDIS_HOST = redis


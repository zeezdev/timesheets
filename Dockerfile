FROM python:3.11-slim

WORKDIR /app

COPY ./*.py .
COPY ./tests ./tests
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

VOLUME /app/db

EXPOSE 8874

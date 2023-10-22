FROM python:3.11-slim

WORKDIR /app

COPY ./*.py .
# TODO: exclude tests in the production
COPY ./tests ./tests
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

VOLUME /db
VOLUME /app

EXPOSE 8874

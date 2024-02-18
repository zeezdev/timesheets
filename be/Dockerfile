FROM python:3.11-slim

WORKDIR /app

COPY ./*.py .
COPY ./alembic .
# TODO: exclude tests in the production
COPY ./tests .
COPY alembic.ini .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

VOLUME /db
VOLUME /app

EXPOSE 8874

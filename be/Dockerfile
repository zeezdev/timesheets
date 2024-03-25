FROM python:3.11-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py .
COPY alembic.ini .
COPY alembic ./alembic
COPY pytest.ini .
COPY tests ./tests

VOLUME /db
VOLUME /app

EXPOSE 8874

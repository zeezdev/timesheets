FROM node:16.14.2-slim As builder

WORKDIR /usr/src/app

COPY ts/package.json ts/package-lock.json ./

RUN npm install

COPY ts .

RUN npm run build

FROM unit:1.32.0-python3.11

COPY unit.init.sh   /docker-entrypoint.d/
COPY --from=builder /usr/src/app/dist/ts/ /www/static/

WORKDIR /app

COPY be/*.py .
COPY be/alembic ./alembic
COPY be/alembic.ini .
COPY be/requirements.txt .
COPY unit.config.json /docker-entrypoint.d/config.json

RUN pip install --no-cache-dir -r requirements.txt

VOLUME /db

EXPOSE 8874 8875

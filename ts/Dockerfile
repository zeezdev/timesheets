FROM node:16.14.2-slim

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

VOLUME /app

EXPOSE 8875

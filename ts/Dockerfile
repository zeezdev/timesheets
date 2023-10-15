FROM node:16.14.2-slim

WORKDIR /app/fe

COPY ./*.json .

RUN npm install

COPY ./src ./src

#RUN npm run build

EXPOSE 8875

CMD ["npm", "start"]

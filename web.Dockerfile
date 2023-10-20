FROM node:16.14.2-slim As builder

WORKDIR /usr/src/app

COPY ts/package.json ts/package-lock.json ./
COPY nginx/proxy_params ./
COPY nginx/templates/default.conf.template ./

RUN npm install

COPY ts .

RUN npm run build --prod

FROM nginx:1.25.2-alpine

COPY --from=builder /usr/src/app/proxy_params /etc/nginx/proxy_params
COPY --from=builder /usr/src/app/dist/ts/ /usr/share/nginx/html
COPY --from=builder /usr/src/app/default.conf.template /etc/nginx/templates/default.conf.template

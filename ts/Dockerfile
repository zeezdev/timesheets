FROM node:16.14.2-slim

WORKDIR /app

# Install Google Chrome for Angular tests
RUN apt-get update --fix-missing && apt-get -y upgrade &&  \
    apt-get install gnupg wget -y && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /etc/apt/trusted.gpg.d/google-archive.gpg && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && \
    apt-get update && \
    apt-get install google-chrome-stable -y --no-install-recommends && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /src/*.deb

COPY package.json package-lock.json ./

RUN npm install

COPY . .

VOLUME /app

EXPOSE 8875

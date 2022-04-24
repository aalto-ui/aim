FROM node:16.14.2-alpine

WORKDIR /usr/src/app

COPY ["./frontend/package.json",  "./frontend/package-lock.json*", "./"]

RUN npm install

USER node

COPY ./frontend ./
COPY ./metrics.json ../

CMD ["node", "build/build.js"]

FROM node:14.17.0-alpine

WORKDIR /home/node/app

COPY ./frontend ./

COPY ./metrics.json ../

RUN apk add --no-cache git && npm ci

USER node

CMD ["node", "build/build.js"]

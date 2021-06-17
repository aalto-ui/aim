FROM node:14.17.0-alpine as builder

WORKDIR /usr/src/app

# Install dependencies
COPY ["./frontend/package.json",  "./frontend/package-lock.json*", "./"]
RUN npm install

# Copy source files
COPY ./frontend ./
COPY ./metrics.json ../

# Build production version
RUN node build/build.js

######################## Second stage

FROM nginx:1.21-alpine

# Copy app
COPY --from=builder /usr/src/app/dist /usr/share/nginx/html

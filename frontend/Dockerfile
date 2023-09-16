FROM node:18-alpine as build

WORKDIR /app
COPY . .
RUN npm install
RUN npm run build

ENTRYPOINT npm run serve -- --host 0.0.0.0 --port ${PORT}

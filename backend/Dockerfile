FROM python:3.8-alpine3.13

WORKDIR /usr/src/app
COPY . .
RUN apk add build-base
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
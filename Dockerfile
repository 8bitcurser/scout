FROM python:3

WORKDIR /usr/src/app
COPY . .

RUN apt -y update && apt -y install npm
RUN npm install vue
RUN pip3 install -r requirements.txt
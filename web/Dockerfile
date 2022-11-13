FROM python:alpine

WORKDIR /usr/src/app

COPY . .

# RUN apk update
RUN apk add musl-dev
RUN apk add linux-headers
RUN apk add gcc

# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn


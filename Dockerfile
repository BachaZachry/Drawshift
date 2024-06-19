FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

# Install postgres client
RUN apk add --update --no-cache postgresql-client

# Install individual dependencies
# so that we could avoid installing extra packages to the container
RUN apk add --update --no-cache --virtual .tmp-build-deps \
	gcc libc-dev linux-headers postgresql-dev musl-dev python3-dev libffi-dev openssl-dev cargo

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Remove dependencies
RUN apk del .tmp-build-deps


ADD ./ /app/

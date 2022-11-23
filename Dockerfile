FROM python:3.10-alpine

WORKDIR /aiblogger

# python can't write .pyc files on disk
ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONBUFFERED=1

COPY . .

RUN apk add --update --no-cache \
	&& pip install --no-cache-dir -r requirements.txt
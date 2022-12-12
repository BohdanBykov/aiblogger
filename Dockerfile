FROM python:3.10-alpine

COPY . /aiblogger

# python can't write .pyc files on disk
ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONBUFFERED=1

RUN apk add --update --no-cache \
	&& pip install --no-cache-dir -r aiblogger/requirements.txt
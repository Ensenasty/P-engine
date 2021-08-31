FROM python:3.9-slim

ENV PYTHHONBUFFERED True
ENV DEBIAN_FRONTEND=noninteractive
ENV APP_HOME /app

RUN apt update && apt -yq upgrade && apt-get -yq install gettext build-essential

WORKDIR $APP_HOME
COPY . ./
RUN pip install --no-cache-dir  -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 p-engine:app


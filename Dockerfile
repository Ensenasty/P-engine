FROM python:3-buster

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt -yq upgrade && apt-get -yq install gettext build-essential

WORKDIR /app/
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT python3 ./bot.py

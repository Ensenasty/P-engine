FROM python:3.9-alpine
LABEL "club.ensenasty.p-engine.mamtaomer"="dev@ensenasty.club"
LABEL "club.ensenasty.p-engine.version"="0.1"

ENV PYTHHONBUFFERED True
ENV APP_HOME /app

WORKDIR $APP_HOME
COPY . ./
RUN pip install --no-cache-dir  -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 p-engine:app


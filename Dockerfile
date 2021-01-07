FROM python:3.8.6-alpine
LABEL author="Sergei Simonov" email="simons2007@yandex.ru" version="0.0.1"
ENV APP=/app
WORKDIR ${APP}
RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
COPY foodgram/. .
RUN pip install -r requirements.txt --no-cache-dir 
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000

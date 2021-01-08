FROM python:3.8.6-alpine
LABEL author="Sergei Simonov" email="simons2007@yandex.ru" version="0.0.1"
ENV APP=/app
WORKDIR ${APP}
RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev \
    postgresql-dev jpeg-dev zlib-dev libjpeg
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir 
COPY foodgram/. .

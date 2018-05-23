FROM python:3.6-jessie

RUN useradd -ms /bin/bash ark

ENV DJANGO_SETTINGS_MODULE=app.settings \
    PYTHONPATH=/usr/src/code/src

RUN apt-get update && \
    apt-get install -y postgresql

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pip install pipenv
RUN pipenv install --system

ADD . /usr/src/code
WORKDIR /usr/src/code

RUN django-admin collectstatic --no-input

USER ark

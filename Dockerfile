FROM python:3.6-jessie

RUN useradd -ms /bin/bash ark

ADD . /usr/src/code
WORKDIR /usr/src/code

ENV DJANGO_SETTINGS_MODULE=app.settings \
    PYTHONPATH=/usr/src/code/src

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pip install pipenv
RUN pipenv install --system

RUN django-admin collectstatic --no-input

USER ark

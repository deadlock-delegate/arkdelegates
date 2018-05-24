FROM python:3.6-jessie

RUN useradd -ms /bin/bash ark

ENV DJANGO_SETTINGS_MODULE=app.settings \
    PYTHONPATH=/usr/src/code/src

RUN apt-get update && \
    apt-get install -y postgresql

COPY requirements.txt .

RUN pip install pip-tools==2.0.2
RUN pip-sync requirements.txt

ADD . /usr/src/code
WORKDIR /usr/src/code

RUN django-admin collectstatic --no-input

USER ark

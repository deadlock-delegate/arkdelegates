FROM python:3.6-jessie

RUN useradd -ms /bin/bash ark

ENV DJANGO_SETTINGS_MODULE=app.settings \
    PYTHONPATH=/app/src \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y postgresql && \
    apt-get install -y apt-transport-https && \
    apt-get install -y build-essential && \
    apt-get install gcc g++ make

# install nodejs
RUN apt-get clean && \
    curl -sL https://deb.nodesource.com/setup_8.x | bash && \
    apt-get install -y nodejs

COPY requirements.txt .

RUN pip install pip-tools==2.0.2
RUN pip-sync requirements.txt

COPY package.json /app/package.json
COPY package-lock.json /app/package-lock.json
COPY static-source /app/static-source
COPY webpack.config.js /app/webpack.config.js
COPY .eslintrc.json /app/.eslintrc.json

WORKDIR /app

RUN npm install
RUN npm run-script build:production

ADD . /app

RUN django-admin collectstatic --no-input

USER ark

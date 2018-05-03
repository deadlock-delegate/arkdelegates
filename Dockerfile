FROM python:3.6-jessie

RUN useradd -ms /bin/bash ark

ADD . /usr/src/code
WORKDIR /usr/src/code

ENV DJANGO_SETTINGS_MODULE=app.settings \
    PYTHONPATH=/usr/src/code/src \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y postgresql && \
    apt-get install -y apt-transport-https && \
    apt-get install -y build-essential && \
    apt-get install gcc g++ make

# install nodejs
RUN apt-get clean && \
    curl -sL https://deb.nodesource.com/setup_8.x | bash

# install yarn
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
    apt-get update && apt-get install -y yarn

COPY requirements.txt .

RUN pip install pip-tools==2.0.2
RUN pip-sync requirements.txt

ADD . /usr/src/code
WORKDIR /usr/src/code

COPY package.json /usr/src/code/package.json
COPY yarn.lock /usr/src/code/yarn.lock
RUN yarn install
RUN yarn build:production

RUN django-admin collectstatic --no-input

USER ark

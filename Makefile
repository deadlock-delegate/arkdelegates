.PHONY: build
build:
	docker-compose build
	make migrate
	make setup-static
	make build-static

up:
	docker-compose up

start:
	docker-compose run --rm --service-ports web

migrations:
	docker-compose run web django-admin makemigrations

migrate:
	docker-compose run web django-admin migrate

superuser:
	docker-compose run web django-admin createsuperuser

updatestats:
	docker-compose run web django-admin update-stats

syncdelegates:
	docker-compose run web django-admin sync-delegates

collectstatic:
	docker-compose run web django-admin collectstatic

shell:
	docker-compose run web django-admin shell

bash:
	docker-compose run web bash

lint:
	docker-compose run web flake8 .

setup-static:
	yarn

build-static:
	yarn build

watch:
	yarn watch

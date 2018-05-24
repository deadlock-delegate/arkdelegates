build:
	docker-compose build

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

pipcompile:
	docker-compose run web pip-compile --generate-hashes requirements.in

pipcompile-local:
	pip-compile --generate-hashes requirements.in

lint:
	docker-compose run web flake8 .

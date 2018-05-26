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

data-shell:
	docker-compose run web django-admin shell_plus

bash:
	docker-compose run web bash

lint:
	docker-compose run web flake8 .

pip-compile:
	docker-compose run web pip-compile requirements.in

test:
	docker-compose run web py.test -v -s $(ARGS)
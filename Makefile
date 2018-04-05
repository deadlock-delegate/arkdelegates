build:
	docker-compose build

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

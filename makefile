ifneq (,$(wildcard ./.env))
	include .env
	export
	ENV_FILE_PARAM = --env-file .env

endif


build:
	docker compose up --build -d --remove-orphans

up:	
	docker compose up -d

down:
	docker compose down

show-logs:
	docker compose logs


migrate:
	docker compose exec web python manage.py migrate

makemigrations:
	docker compose exec web python manage.py makemigrations

check:
	docker compose exec web python manage.py check

migrate_elasticsearch:
	docker compose exec web python manage.py search_index --rebuild

createsuperuser:
	docker compose exec web python manage.py createsuperuser

collectstatic:
	docker compose exec web python manage.py collectstatic --no-input --clear

django-check:
	docker compose exec web python manage.py check

init_db:
	docker compose exec web python manage.py db_init 30

shell:	
	docker compose exec web python manage.py shell_plus

down-v:
	docker compose down -v 

volume:
	docker volume inspect sms-app_postgres_data


rental-db:
	docker compose exec postgres-db psql --username=miclem --dbname=sms

test:
	docker compose exec web pytest -p no:warnings --cov=.

test-html:
	docker compose exec web pytest -p no:warnings --cov=. --cov-report html

flake8:
	docker compose exec web flake8

black-check:
	docker compose exec web black --check --exclude=migrations .

black-diff:
	docker compose exec web black --diff --exclude=migrations .

black:
	docker compose exec web black --exclude=migrations .

isort-check:
	docker compose exec web isort . --check-only --skip env --skip migrations

isort-diff:
	docker compose exec web isort . --diff --skip env --skip  migrations
	
isort:
	docker compose exec web isort . --skip env --skip migrations

lint: 
	flake8 black-check isort-check

config:
	docker compose config

watch:
	docker compose exec web watchmedo shell-command --patterns="*.py" --recursive --command='make lint test' .



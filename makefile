export PYTHONPATH=.

format:
	ruff format .
	ruff check . --fix

run_local:
	uvicorn --factory main:create_app --reload

up:
	docker-compose up

build:
	docker-compose build

bash:
	docker-compose run --rm web bash

test:
	docker-compose run --rm web pytest tests

test_local:
	pytest tests
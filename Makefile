SRC = app
TESTS = tests/functional

install:
	poetry install

up:
	docker compose --env-file .env up --build

tests:	
	poetry run python3 tests/functional/test_form_template.py

stop:
	docker compose stop

prune:
	docker container prune -f
	docker volume prune -f
	docker volume rm ecom_test_task_mongo_data

format:  
	poetry run black ${SRC}
	poetry run black ${TESTS}
	poetry run isort ${SRC}
	poetry run isort ${TESTS}
	poetry run autoflake --in-place --remove-unused-variables --remove-all-unused-imports -r ${SRC}
	poetry run autoflake --in-place --remove-unused-variables --remove-all-unused-imports -r ${TESTS}

lint:
	poetry run flake8 ${SRC}
	poetry run flake8 ${TESTS}
	poetry run mypy ${SRC}
	poetry run flake8 ${TESTS}
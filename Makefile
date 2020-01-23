
SERVICE_NAME ?= "common"

all:
	@run_test

clean_cache:
	find . | grep -E "\(__pycache__|\.pyc|\.pyo$\)" | xargs rm -rf && \
	rm -rf ./htmlcov

clean: clean_cache

test: clean_cache
	pytest --pyargs -v ./

coverage: clean_cache
	pytest --pyargs --cov=./ --cov-config=.coveragerc --cov-report=html

up:
	docker-compose up -d --build

tty:
	docker exec -it $(SERVICE_NAME) /bin/bash

down:
	docker-compose down

run_test:
	docker exec -it $(SERVICE_NAME) make test

run_coverage:
	docker exec -it $(SERVICE_NAME) make coverage


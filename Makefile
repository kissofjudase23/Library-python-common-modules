
SERVICE_NAME ?= "library-python-common-modules"

all:
	@run_test

clean_cache:
	find . | grep -E "\(__pycache__|\.pyc|\.pyo$\)" | xargs rm -rf && \
	rm -rf ./htmlcov

test: clean_cache
	pytest --pyargs -v ./

coverage: clean_cache
	pytest --pyargs --cov-report=html --cov-config=.coveragerc --cov=./

up:
	docker-compose up -d --build

attach:
	docker exec -it $(SERVICE_NAME) make test

down:
	docker-compose down

run_test:
	docker exec -it $(SERVICE_NAME) make test

run_coverage:
	docker exec -it $(SERVICE_NAME) make coverage


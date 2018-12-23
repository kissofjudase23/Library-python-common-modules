include MK/docker.mk

# docker environment
HOST_PATH  ?= "$(shell pwd)"
GUEST_PATH ?= "/tmp/$(shell basename $(HOST_PATH))"
DOCKERFILE ?= "dockerfile"
DOCKER_REPO ?= "$(shell basename $(HOST_PATH) | tr '[:upper:]' '[:lower:]')"
DOCKER_TAG  ?= "develop"


all:
	@run_test

clean_cache:
	find . | grep -E "\(__pycache__|\.pyc|\.pyo$\)" | xargs rm -rf &&
	rm -rf ./htmlcov

# build a docker images for develop
build_dev:
	@make docker_build

run_dev_inspect:
	@make docker_inspect

run_dev_stop:
	@make docker_stop

# create a container to debug (SSH loging)
run_debug:
	@make docker_run_debug

# run coverage test in docker
run_dev_coverage: clean_cache
	@make docker_run TEST_COMMAND="pytest --pyargs --cov-report=html --cov-config=.coveragerc --cov=./"
	
# run test in host
coverage: clean_cache
	pytest --pyargs --cov-report=html --cov-config=.coveragerc --cov=./

# run test in docker 
run_dev_test: clean_cache
	@make docker_run TEST_COMMAND="pytest --pyargs -v ./"	

test: clean_cache
	pytest --pyargs -v ./
	



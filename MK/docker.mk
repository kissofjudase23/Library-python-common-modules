
DEFAULT_SHELL ?= "/bin/bash"

# build a docker image from the docker file
docker_build:
	docker build \
		-t $(DOCKER_REPO):$(DOCKER_TAG) \
		--build-arg work_dir=$(GUEST_PATH) \
		-f $(DOCKERFILE) .

# create a container and allocate a pseudo tty for debug
# note: assume the ENTRYPOINT=["/bin/bash", "-c""]
docker_run_debug:
	docker run --rm \
		-v $(HOST_PATH):$(GUEST_PATH) \
		-i --tty $(DOCKER_REPO):$(DOCKER_TAG) \
		$(DEFAULT_SHELL)

# create a container and run your test command via CMD
# note: CMD should match the setting of ENTRYPOINT in your dockerfile
docker_run:
	docker run --rm \
		-v $(HOST_PATH):$(GUEST_PATH) \
		$(DOCKER_REPO):$(DOCKER_TAG) $(TEST_COMMAND)

# run docker with daemon mode
docker_run_daemon:
	docker run --rm \
		-d \
		-v $(HOST_PATH):$(GUEST_PATH) \
		-p $(HOST_PORT):$(GUEST_PORT) \
		$(DOCKER_REPO):$(DOCKER_TAG) $(TEST_COMMAND)

docker_inspect:
	docker ps -a | \
	grep "$(DOCKER_REPO):$(DOCKER_TAG)" | \
	awk 'BEGIN {FS= " "} NR==1 {print $$1}' | \
	xargs docker inspect

docker_stop:
	docker ps -a | \
	grep "$(DOCKER_REPO):$(DOCKER_TAG)" | \
	awk 'BEGIN {FS= " "} NR==1 {print $$1}' | \
	xargs docker stop

# remove dangling docker images
docker_rmi_dangling:
	docker images -aq \
		--no-trunc \
		--filter "dangling=true" | xargs docker rmi

# remove all docker images, use this command carefully
docker_rmi_all:
	docker images -aq \
		--no-trunc | xargs docker rmi



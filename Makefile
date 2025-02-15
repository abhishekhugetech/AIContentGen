include .env

VERSION=v1

build_and_push:
	docker login -u ${DOCKER_USER} --password-stdin <<<${DOCKER_PAT}
	docker build -t contentservicepython:${VERSION} -f ./python/Dockerfile ./python
	docker tag contentservicepython:${VERSION} ${DOCKER_USER}/contentservicepython:${VERSION}
	docker push ${DOCKER_USER}/contentservicepython:${VERSION}

run_local:
	docker compose -f docker-compose-local.yml up --build

# docker pull magtapptest/contentservicepython:v1
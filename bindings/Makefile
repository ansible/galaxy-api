.PHONY: build
build:
	docker run --rm -u "$(shell id -u)" -v "${PWD}:/local" \
		openapitools/openapi-generator-cli generate \
		-i /local/openapi.yaml \
		-g python \
		-o /local/galaxy-pulp \
		--additional-properties=packageName=galaxy_pulp,projectName=galaxy-pulp



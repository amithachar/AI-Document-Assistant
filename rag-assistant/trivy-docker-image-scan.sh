#!/bin/bash

dockerimage=$(cat Dockerfile | grep "FROM" | awk '{print $2}')
echo "Docker image: $dockerimage"


if [[ -z "$dockerimage" ]]; then
    echo "Error: Docker image not found in Dockerfile"
    exit 1
fi

echo "Scaning the docker image: $dockerimage"

trivy image --exit-code 0 --severity HIGH $dockerimage

trivy image --exit-code 1 --severity CRITICAL $dockerimage


exit_code=$?

echo "Exit code: $exit_code"

if [[ $exit_code == 1 ]]; then
    echo "Image scanning failed. vulnerabilties found in the image"
    exit 1
else
    echo "Image scanning passed. No vulnerabilties found in the image"
fi
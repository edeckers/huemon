#!/usr/bin/env bash

function cd_to_root_directory () {
  cd `dirname ${0}`/../../
}

function build_and_publish_docker_image () {
  cd_to_root_directory

  echo "Building and publishing Docker image ghcr.io/edeckers/huemon:2.0.3"
  docker buildx build . --platform linux/amd64,linux/arm64,linux/arm/v7 -t ghcr.io/edeckers/huemon:2.0.3 --push
  echo "Built and published Docker image ghcr.io/edeckers/huemon:2.0.3"
}

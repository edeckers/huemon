#!/usr/bin/env bash

function cd_to_root_directory () {
  cd `dirname ${0}`/../../
}

function build_and_publish_docker_image () {
  cd_to_root_directory

  echo "Building and publishing Docker image edeckers/huemon:0.8.0"
  docker buildx build . --platform linux/amd64,linux/arm64,linux/arm/v7 -t edeckers/huemon:0.8.0 --push
  echo "Built and published Docker image edeckers/huemon:0.8.0"
}

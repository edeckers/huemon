#!/usr/bin/env bash

function cd_to_root_directory () {
  cd `dirname ${0}`/../../
}

function build_docker_image () {
  cd_to_root_directory

  echo "Building docker image edeckers/huemon:0.6.0"
  docker buildx build . --platform linux/amd64,linux/arm64,linux/arm/v7 -t edeckers/huemon:0.6.0 --push
  echo "Built docker image edeckers/huemon:0.6.0"
}

function push_docker_image () {
  cd_to_root_directory

  echo "Pushing docker image edeckers/huemon:0.6.0"
  docker push edeckers/huemon:0.6.0
  echo "Pushed docker image edeckers/huemon:0.6.0"
}

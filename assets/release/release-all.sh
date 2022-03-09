#!/usr/bin/env bash

function cd_to_root_directory () {
  cd `dirname ${0}`/../../
}

function publish_semantic_release () {
  echo "Publishing release"
  poetry run semantic-release publish
  echo "Published release"
}

function build_dist () {
  poetry build
}

cd_to_root_directory

publish_semantic_release

source assets/release/release-docker.sh

build_dist
build_and_publish_docker_image

#!/usr/bin/env bash

function cd_to_root_directory () {
  cd `dirname ${0}`/../../
}

function publish_semantic_release () {
  echo "Publishing release"
  poetry run semantic-release publish
  echo "Published release"
}

function create_semantic_release () {
  echo "Creating semantic release"
  poetry run semantic-release version
  poetry build
  echo "Created semantic release"
}

cd_to_root_directory

create_semantic_release

source assets/release/release-docker.sh
build_docker_image

publish_semantic_release
push_docker_image
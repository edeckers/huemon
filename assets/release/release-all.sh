#!/usr/bin/env bash

function cd_to_root_directory () {
  cd `dirname ${0}`/../../
}

function publish_semantic_release () {
  echo "Publishing release"
  publish_result=`p run semantic-release publish 2>&1`
  error_code=`echo $?`
  is_error_code=`[ -z ${error_code} ] && echo 1 || echo 0`
  
  no_release_count=`echo "${publish_result}" | grep -cim1 "no release"`
  is_release=`[ -z ${no_release_count} ] && echo 1 || echo 0`

  echo "${publish_result}"

  if [[ ${is_error_code} -eq 1 || ${is_release} -ne 1 ]]; then
    echo "has error code: ${is_error_code}"
    echo "is release created: ${is_release}"

    echo "Received error code or no release was created. Aborting."
    exit 0
  fi

  echo "Published release"
}

function build_dist () {
  p build
}

cd_to_root_directory

source src/bin/shared.sh

publish_semantic_release

source assets/release/release-docker.sh

build_dist
build_and_publish_docker_image

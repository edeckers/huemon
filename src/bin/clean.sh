#!/usr/bin/env bash

function cd_to_source_directory () {
  cd `dirname ${0}`/..
}

function clean () {
  find . -type d -name "__pycache__" | xargs rm -rf {};
  rm -rf ${INSTALL_STAMP_PATH} .coverage .mypy_cache
}

cd_to_source_directory

source bin/shared.sh

clean

#!/usr/bin/env bash

function cd_to_source_directory () {
  cd `dirname ${0}`/..
}

function install_git_hooks () {
  pre-commit install
  pre-commit install --hook-type commit-msg
}

function install () {
  p install
  touch ${INSTALL_STAMP_PATH}
}

cd_to_source_directory

source bin/shared.sh

install_git_hooks
install

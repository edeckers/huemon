#!/usr/bin/env bash

function cd_to_source_directory() {
  cd `dirname ${0}`/..
}

function install_git_hooks() {
  pre-commit install
  pre-commit install --hook-type commit-msg
}

function install_required_packages() {
  pip3 install -r requirements.txt
}

cd_to_source_directory
install_required_packages
install_git_hooks

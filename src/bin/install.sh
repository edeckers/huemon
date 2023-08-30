#!/usr/bin/env bash

function cd_to_source_directory () {
  cd `dirname ${0}`/..
}

function install_git_hooks () {
  p run pre-commit install
  p run pre-commit install --hook-type commit-msg
}

function install_poetry () {
  if [ -z ${POETRY} ]; then
    curl -sSL https://install.python-poetry.org/ | python

    try_source_env
  fi
}

function install () {
  p install
}

cd_to_source_directory

source bin/shared.sh

install_poetry
install
install_git_hooks

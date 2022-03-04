#!/usr/bin/env bash

INSTALL_STAMP_PATH='.install.stamp'

function poetry_path () {
  if [ -z ${POETRY} ]; then
    source $HOME/.poetry/env
  fi

  echo `command -v poetry 2> /dev/null`
}

function assert_poetry_exists () {
  if [ -z `poetry_path` ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
}

function p () {
  assert_poetry_exists
  `poetry_path` ${@}
}

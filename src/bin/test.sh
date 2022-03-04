#!/usr/bin/env bash

function cd_to_source_directory() {
  cd `dirname ${0}`/..
}

function run_tests() {
  p run nox
}

cd_to_source_directory

source bin/shared.sh

run_tests

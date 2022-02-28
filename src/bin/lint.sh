#!/usr/bin/env bash

function cd_to_source_directory() {
  cd `dirname ${0}`/..
}

function run_linter() {
  pylint huemon
  pylint tests
}

cd_to_source_directory
run_linter

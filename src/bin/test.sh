#!/usr/bin/env bash

function cd_to_source_directory() {
  cd `dirname ${0}`/..
}

function run_tests() {
  python3 -m unittest discover tests -b
}

cd_to_source_directory
run_tests

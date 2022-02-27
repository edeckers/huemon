#!/usr/bin/env bash

function cd_to_source_directory() {
  cd `dirname ${0}`/..
}

function run_initializer() {
  pip3 install -r requirements.txt
}

cd_to_source_directory
run_initializer

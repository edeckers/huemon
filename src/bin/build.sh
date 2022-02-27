#!/usr/bin/env bash

function cd_to_source_directory() {
  cd `dirname ${0}`/..
}

function create_meta_files() {
  cp ../README.md README
}

function clean_meta_files() {
  rm README
}

function create_dist() {
  ./setup.py sdist
}

cd_to_source_directory
create_meta_files
create_dist
clean_meta_files

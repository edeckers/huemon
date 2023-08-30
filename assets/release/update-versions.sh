#!/usr/bin/env bash

function cd_to_root_directory () {
  cd `dirname ${0}`/../../
}

cd_to_root_directory

source src/bin/shared.sh

VERSION=$(cat pyproject.toml | grep "^version *= *\"[0-9]\.[0-9]\.[0-9]\"$" | sed -r 's/^version *= *\"(.*)\"$/\1/')
NEXT_VERSION=$(p run semantic-release version --print)

echo "Replacing all occurences of ${VERSION} with ${NEXT_VERSION}"

sed -i"" "s/edeckers\/huemon:${VERSION}/edeckers\/huemon:${NEXT_VERSION}/g" assets/release/release-docker.sh
sed -i"" "s/edeckers\/huemon:${VERSION}/edeckers\/huemon:${NEXT_VERSION}/g" docker-compose.yml
sed -i"" "s/ARG HUEMON_VERSION=${VERSION}/ARG HUEMON_VERSION=${NEXT_VERSION}/g" Dockerfile

echo "Replaced all occurrences of ${VERSION} with ${NEXT_VERSION}"
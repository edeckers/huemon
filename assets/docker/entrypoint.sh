#!/usr/bin/env bash

# inspired by https://github.com/sameersbn/docker-gitlab/blob/master/entrypoint.sh

set -e -u -o pipefail

case ${1} in
  agent|discover|value)
    case ${1} in
      agent)
        python3 -m huemon agent ${2}
        ;;
      discover)
        python3 -m huemon discover ${2}
        ;;
      value)
        python3 -m huemon ${2} ${3} ${4}
        ;;
    esac
    ;;
  help)
    echo "Available options:"
    echo " agent     - Start agent mode"
    echo " discover  - Discover resources"
    echo " value     - Read resource value"
    echo " help      - Displays the help"
    echo " [command] - Execute the specified command, eg. bash."
    ;;
  *)
    exec "$@"
    ;;
esac

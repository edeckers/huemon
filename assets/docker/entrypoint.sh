#!/usr/bin/env bash

# inspired by https://github.com/sameersbn/docker-gitlab/blob/master/entrypoint.sh

set -e -u -o pipefail

case ${1} in
  agent|discover|install|value)
    case ${1} in
      agent)
        python3 -m huemon agent ${2}
        ;;
      discover)
        python3 -m huemon discover ${2}
        ;;
      install)
        python3 -m huemon install_available commands
        python3 -m huemon install_available discoveries
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
    echo " install   - Read resource value"
    echo " value     - Read resource value"
    echo " help      - Displays the help"
    echo " [command] - Execute the specified command, eg. bash."
    ;;
  *)
    exec "$@"
    ;;
esac

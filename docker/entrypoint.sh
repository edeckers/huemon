#!/usr/bin/env bash

# set -e, -u, -x, -o pipefail

case ${1} in
  app:discover|app:install|app:value)
    case ${1} in
      app:discover)
        python3 -m huemon discover ${2}
        ;;
      app:install)
        python3 -m huemon install_available commands
        python3 -m huemon install_available discoveries
        ;;
      app:value)
        python3 -m huemon ${2} ${3} ${4}
        ;;
    esac
    ;;
  app:help)
    echo "Available options:"
    echo " app:discover - Discover resources"
    echo " app:value    - Read resource value"
    echo " app:install  - Read resource value"
    echo " app:help     - Displays the help"
    echo " [command]    - Execute the specified command, eg. bash."
    ;;
  *)
    exec "$@"
    ;;
esac

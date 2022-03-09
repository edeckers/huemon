#!/usr/bin/env bash

set -e -u -o pipefail

SYSTEMD_CONFIG_PATH="${HOME}/.config/systemd/user"
TARGET_PATH="${SYSTEMD_CONFIG_PATH}/huemon.service"

function cd_to_assets_directory () {
  cd `dirname ${0}`/..
}

function uninstall_service_and_reload_systemd () {
  echo "Starting deinstallation of Huemon-service"

  if [ ! -f "${TARGET_PATH}" ]; then
    echo "The file ${TARGET_PATH} doesn't exist. Aborting."
    exit 1
  fi

  systemctl --user stop huemon
  systemctl --user disable huemon

  echo "Removing ${TARGET_PATH}"
  sudo rm "${TARGET_PATH}"
  echo "Removed ${TARGET_PATH}"

  systemctl --user daemon-reload
  echo "Finished deistallation of Huemon-service"
}

function install_service_and_reload_systemd () {
  echo "Starting installation of Huemon-service"

  if [ -f "${TARGET_PATH}" ]; then
    echo "The file ${TARGET_PATH} already exists. Aborting."
    exit 1
  fi

  mkdir -p "${SYSTEMD_CONFIG_PATH}"

  echo "Copying Huemon-service to ${TARGET_PATH}"
  sudo cp systemd/huemon.service "${TARGET_PATH}"
  echo "Copied Huemon-service to ${TARGET_PATH}"

  systemctl --user daemon-reload


  systemctl --user enable huemon
  systemctl --user start huemon
  echo "Finished installation of Huemon-service"
}

cd_to_assets_directory

case ${1} in
  install|uninstall)
    case ${1} in
      install)
        install_service_and_reload_systemd
        ;;
      uninstall)
        uninstall_service_and_reload_systemd
        ;;
    esac
    ;;
  *)
    echo "Available options:"
    echo " install   - Install the Huemon Systemd service"
    echo " uninstall - Uninstall the Huemon Systemd service"
    echo " help      - Displays the help"
    ;;
esac

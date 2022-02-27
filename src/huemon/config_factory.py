# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import sys

from os import environ, path
from pathlib import Path
from genericpath import isfile

import yaml

from huemon.const import EXIT_FAIL

CONFIG_PATH_LOCAL = path.join(str(Path(__file__).parent), "config.yml")
CONFIG_PATH_ENV_VARIABLE = environ.get("HUEMON_CONFIG_PATH")

CONFIG_PATHS_ORDERED_PREFERENCE = list(filter(lambda p: p, [
    CONFIG_PATH_ENV_VARIABLE,
    CONFIG_PATH_LOCAL,
]))


def __first_existing_config_file():
  for config_path in CONFIG_PATHS_ORDERED_PREFERENCE:
    if isfile(config_path):
      return config_path

  return None


def create_config():
  maybe_config_path = __first_existing_config_file()
  if not maybe_config_path:
    print(
        f"No configuration file found in: {','.join(CONFIG_PATHS_ORDERED_PREFERENCE)}")
    sys.exit(EXIT_FAIL)

  with open(maybe_config_path, "r") as file:
    return yaml.safe_load(file.read())

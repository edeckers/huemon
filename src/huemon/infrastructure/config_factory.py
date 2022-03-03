# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from os import environ, path
from pathlib import Path

import yaml
from genericpath import isfile

from huemon.util import exit_fail

CONFIG_PATH_LOCAL = path.join(str(Path(__file__).parent.parent), "config.yml")
CONFIG_PATH_ENV_VARIABLE = environ.get("HUEMON_CONFIG_PATH")

CONFIG_PATHS_ORDERED_PREFERENCE = list(
    filter(
        None,
        [
            CONFIG_PATH_ENV_VARIABLE,
            CONFIG_PATH_LOCAL,
        ],
    )
)


def __first_existing_config_file():
    for config_path in CONFIG_PATHS_ORDERED_PREFERENCE:
        if isfile(config_path):
            return config_path

    return None


def create_config():
    maybe_config_path = __first_existing_config_file()
    if not maybe_config_path:
        exit_fail(
            "No configuration file found in %s",
            ",".join(CONFIG_PATHS_ORDERED_PREFERENCE),
        )

    with open(maybe_config_path, "r") as file:
        return yaml.safe_load(file.read())

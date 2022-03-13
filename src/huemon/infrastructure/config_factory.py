# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from os import environ, path
from pathlib import Path

import yaml
from genericpath import isfile

from huemon.utils.errors import exit_fail
from huemon.utils.monads.maybe import Maybe, nothing

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


def __first_existing_config_file() -> Maybe[str]:
    for config_path in CONFIG_PATHS_ORDERED_PREFERENCE:
        if isfile(config_path):
            return Maybe.of(config_path)

    return nothing


def __read_yaml_file(yaml_path: str):
    with open(yaml_path, "r") as file:
        return yaml.safe_load(file.read())


def create_config() -> dict:
    maybe_config_file = __first_existing_config_file()
    if maybe_config_file.is_nothing():
        exit_fail(
            "No configuration file found in %s",
            ",".join(CONFIG_PATHS_ORDERED_PREFERENCE),
        )

    return __read_yaml_file(maybe_config_file.from_just())

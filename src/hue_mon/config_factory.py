# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from pathlib import Path

import yaml


def create_config():
  with open("/".join([str(Path(__file__).parent), "config.yml"]), "r") as file:
    return yaml.safe_load(file.read())

from pathlib import Path

import yaml


def create_config():
  with open("/".join([str(Path(__file__).parent), "config.yml"]), "r") as file:
    return yaml.safe_load(file.read())

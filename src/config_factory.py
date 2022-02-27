import yaml

from pathlib import Path


def create_config():
  with open("/".join([str(Path(__file__).parent), "config.yml"]), "r") as f:
    return yaml.safe_load(f.read())

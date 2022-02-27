import logging
import logging.config

from config_factory import create_config


def create_logger():
  logging.config.dictConfig(create_config())

  return logging.getLogger("hue")

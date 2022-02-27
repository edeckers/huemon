import logging
import logging.config

from hue_mon.config_factory import create_config


def create_logger():
  logging.config.dictConfig(create_config())

  return logging.getLogger("hue")

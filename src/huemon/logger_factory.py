# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import logging
import logging.config


def bootstrap_logger(config: dict):
  logging.config.dictConfig(config)

  return create_logger()


def create_logger(name="hue"):
  return logging.getLogger(name)

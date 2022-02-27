# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import logging
import logging.config

from hue_mon.config_factory import create_config


def create_logger():
  logging.config.dictConfig(create_config())

  return logging.getLogger("hue")

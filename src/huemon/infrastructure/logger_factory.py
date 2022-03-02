# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import logging
import logging.config

DEFAULT_LOGGER_NAME = "hue"


def bootstrap_logger(config: dict, name=DEFAULT_LOGGER_NAME):
    logging.config.dictConfig(config)

    return create_logger(name)


def create_logger(name=DEFAULT_LOGGER_NAME):
    return logging.getLogger(name)

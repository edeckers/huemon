# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import json
import os
import sys
import tempfile
from fcntl import LOCK_EX, LOCK_NB, flock
from pathlib import Path

from huemon.const import EXIT_FAIL
from huemon.infrastructure.logger_factory import create_logger


def create_local_path(relative_path: str):
    return str(os.path.join(Path(__file__).parent.absolute(), relative_path))


LOG = create_logger()


def __create_plugins_path(plugin_type: str, config: dict, fallback_path: str = None):
    plugins_section_exists = "plugins" in config
    if not plugins_section_exists:
        return fallback_path

    plugin_type_exists = config["plugins"][plugin_type]
    if not plugin_type_exists:
        return fallback_path

    return (
        config["plugins"][plugin_type]["path"]
        if "path" in config["plugins"][plugin_type]
        else fallback_path
    )


def get_command_plugins_path(config: dict, fallback_path: str = None):
    return __create_plugins_path("commands", config, fallback_path)


def get_discovery_plugins_path(config: dict, fallback_path: str = None):
    return __create_plugins_path("discoveries", config, fallback_path)


def exit_fail(message, *arguments):
    LOG.error(message, *arguments)
    print(message % tuple(arguments))

    sys.exit(EXIT_FAIL)


def assert_num_args(expected_number_of_arguments: int, arguments: list, context: str):
    if len(arguments) != expected_number_of_arguments:
        argument_text = "argument" if expected_number_of_arguments == 1 else "arguments"

        exit_fail(
            "Expected exactly %s %s for `%s`, received %s",
            expected_number_of_arguments,
            argument_text,
            context,
            len(arguments),
        )


def assert_exists(expected_values: list, value: str):
    if value not in expected_values:
        exit_fail("Received unknown value `%s` (expected=%s)", value, expected_values)


def cache_output_to_temp(cache_file_path, fn_call):
    tmp_fd, tmp_file_path = tempfile.mkstemp()
    with open(tmp_file_path, "w") as f_tmp:
        f_tmp.write(json.dumps(fn_call()))

    os.close(tmp_fd)

    os.rename(tmp_file_path, cache_file_path)

    with open(cache_file_path) as f_json:
        return json.loads(f_json.read())


def run_locked(lock_file, fn_call):
    with open(lock_file, "w") as f_lock:
        try:
            flock(f_lock.fileno(), LOCK_EX | LOCK_NB)
            LOG.debug("Acquired lock successfully (file=%s)", lock_file)

            return fn_call()
        except BlockingIOError:
            LOG.debug("Failed to acquire lock (file=%s)", lock_file)
        except Exception as error:  # pylint: disable=broad-except
            LOG.debug(
                "Something unexpected went wrong while acquiring lock (file=%s, error=%s)",
                lock_file,
                error,
            )

    return None

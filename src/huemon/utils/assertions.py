# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from huemon.utils.errors import exit_fail


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

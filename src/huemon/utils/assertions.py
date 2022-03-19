# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from typing import List

from huemon.utils.errors import (
    E_CODE_ASSERT_EXISTS,
    E_CODE_ASSERT_NUM_ARGS,
    HueError,
    exit_fail,
)
from huemon.utils.monads.either import Either, left, right


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


def assert_num_args_e(
    expected_number_of_arguments: int, arguments: List[str], context: str
) -> Either[HueError, List[str]]:
    try:
        assert_num_args(expected_number_of_arguments, arguments, context)

        return right(arguments)
    except SystemExit:
        return left(HueError(E_CODE_ASSERT_NUM_ARGS, "FIXME_NUM_ARGS"))


def assert_exists(expected_values: list, value: str):
    if value not in expected_values:
        exit_fail("Received unknown value `%s` (expected=%s)", value, expected_values)


def assert_exists_e(expected_values: list, value: str):
    try:
        assert_exists(expected_values, value)

        return right(value)
    except SystemExit:
        return left(HueError(E_CODE_ASSERT_EXISTS, "FIXME_EXISTS"))

# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from typing import Callable, Generic, List, TypeVar

TA = TypeVar("TA")
TB = TypeVar("TB")
TC = TypeVar("TC")


class Either(Generic[TA, TB]):  # pylint: disable=too-few-public-methods
    value = None


class Left(Either[TA, TB]):  # pylint: disable=too-few-public-methods
    def __init__(self, value: TA):
        self.value = value

    def __str__(self) -> str:
        return f"Left(value={self.value.__str__()})"


class Right(Either[TA, TB]):  # pylint: disable=too-few-public-methods
    def __init__(self, value: TB):
        self.value = value

    def __str__(self) -> str:
        return f"Right(value={self.value.__str__()})"


def bind(em0: Either[TC, TA], map_: Callable[[TA], Either[TC, TB]]) -> Either[TC, TB]:
    return em0 if is_left(em0) else map_(em0.value)


def chain(em0: Either[TC, TA], em1: Either[TC, TB]) -> Either[TC, TB]:
    return bind(em0, lambda _: em1)


def either(
    map_left: Callable[[TA], TC], map_right: Callable[[TB], TC], em0: Either[TA, TB]
) -> TC:
    return map_left(em0.value) if is_left(em0) else map_right(em0.value)


def flat_map(
    em0: Either[TC, TA], map_: Callable[[TA], Either[TC, TB]]
) -> Either[TC, TB]:
    return bind(em0, lambda m0: pure(map_(m0)))


def is_left(em0: Either[TA, TB]) -> bool:
    return isinstance(em0, Left)


def is_right(em0: Either[TA, TB]) -> bool:
    return not is_left(em0)


def lefts(eithers: Either[TA, TB]) -> List[TA]:
    return list(map(lambda either: either.value, filter(is_left, eithers)))


def pure(value: TB) -> Either[TA, TB]:
    return Right(value)


def rights(eithers: Either[TA, TB]) -> List[TB]:
    return list(map(lambda either: either.value, filter(is_right, eithers)))

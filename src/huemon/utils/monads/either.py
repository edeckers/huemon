# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

from argparse import ArgumentTypeError
from typing import Callable, Generic, List, TypeVar, Union, cast

TA = TypeVar("TA")
TB = TypeVar("TB")
TC = TypeVar("TC")
TD = TypeVar("TD")


class Either(Generic[TA, TB]):  # pylint: disable=too-few-public-methods
    value: Union[TA, TB]

    def bind(self, map_: Callable[[TB], Either[TA, TC]]) -> Either[TA, TC]:
        return bind(self, map_)

    def chain(self, em1: Either[TA, TB]) -> Either[TA, TB]:
        return chain(self, em1)

    def discard(self, map_: Callable[[TB], Either[TA, TB]]) -> Either[TA, TB]:
        return self.bind(map_).chain(self)

    def either(self, map_left: Callable[[TA], TC], map_right: Callable[[TB], TC]) -> TC:
        return either(map_left, map_right, self)

    def fmap(self, map_: Callable[[TB], TC]) -> Either[TA, TC]:
        return fmap(self, map_)

    def is_left(self) -> bool:
        return is_left(self)

    def is_right(self) -> bool:
        return is_right(self)

    @staticmethod
    def pure(value: TB) -> Either[TA, TB]:  # pylint: disable=invalid-name
        return pure(value)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Either):
            return False

        if __o.is_left() or self.is_left():
            return __o.is_left() and self.is_left() and __o.value == self.value

        return __o.value == self.value


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
    if is_left(em0):
        return cast(Left[TC, TB], em0)

    result = map_(cast(TA, em0.value))
    if not isinstance(result, Either):
        raise ArgumentTypeError("Bind should return Either")

    return result


def chain(em0: Either[TC, TA], em1: Either[TC, TB]) -> Either[TC, TB]:
    return bind(em0, lambda _: em1)


def either(
    map_left: Callable[[TA], TC], map_right: Callable[[TB], TC], em0: Either[TA, TB]
) -> TC:
    return (
        map_left(cast(TA, em0.value))
        if is_left(em0)
        else map_right(cast(TB, em0.value))
    )


def fmap(em0: Either[TC, TA], map_: Callable[[TA], TB]) -> Either[TC, TB]:
    return bind(em0, lambda m0: pure(map_(m0)))


def is_left(em0: Either[TA, TB]) -> bool:
    return isinstance(em0, Left)


def is_right(em0: Either[TA, TB]) -> bool:
    return not is_left(em0)


def left(value: TA) -> Either[TA, TB]:
    return Left(value)


def lefts(eithers: List[Either[TA, TB]]) -> List[TA]:
    return list(map(lambda either: cast(TA, either.value), filter(is_left, eithers)))


def rights(eithers: List[Either[TA, TB]]) -> List[TB]:
    return list(map(lambda either: cast(TB, either.value), filter(is_right, eithers)))


def right(value: TB) -> Either[TA, TB]:
    return Right(value)


pure = Right  # pylint: disable=invalid-name

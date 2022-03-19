# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

from argparse import ArgumentTypeError
from typing import Callable, List, Tuple, TypeVar, Union, cast

TA = TypeVar("TA")
TB = TypeVar("TB")
TC = TypeVar("TC")


class Either(Tuple[TA, TB]):  # pylint: disable=too-few-public-methods
    value: Union[TA, TB]

    def __new__(cls, _):
        return super(Either, cls).__new__(cls)

    def __init__(self, value: Union[TA, TB]):
        self.value = value

    def __len__(self):
        return 2

    def __iter__(self):
        return (self.if_right(None), self.if_left(None)).__iter__()

    def __or__(self, map_: Callable[[TB], TC]) -> Either[TA, TC]:
        return self.fmap(map_)

    def __ge__(self, map_: Callable[[TB], Either[TA, TC]]) -> Either[TA, TC]:
        return bind(self, map_)

    def bind(self, map_: Callable[[TB], Either[TA, TC]]) -> Either[TA, TC]:
        return bind(self, map_)

    def then(self, em1: Either[TA, TB]) -> Either[TA, TB]:
        return then(self, em1)

    def discard(self, map_: Callable[[TB], Either[TA, TB]]) -> Either[TA, TB]:
        return self.bind(map_).then(self)

    def either(self, map_left: Callable[[TA], TC], map_right: Callable[[TB], TC]) -> TC:
        return either(map_left, map_right, self)

    def fmap(self, map_: Callable[[TB], TC]) -> Either[TA, TC]:
        return fmap(self, map_)

    def if_left(self, fallback: TB) -> TB:
        return if_left(self, fallback)

    def is_left(self) -> bool:
        return is_left(self)

    def if_right(self, fallback: TA) -> TA:
        return if_right(self, fallback)

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


class _Left(Either[TA, TB]):  # pylint: disable=too-few-public-methods
    def __str__(self) -> str:
        return f"Left(value={self.value.__str__()})"


class _Right(Either[TA, TB]):  # pylint: disable=too-few-public-methods
    def __str__(self) -> str:
        return f"Right(value={self.value.__str__()})"


def __id(value):
    return value


def bind(em0: Either[TC, TA], map_: Callable[[TA], Either[TC, TB]]) -> Either[TC, TB]:
    if is_left(em0):
        return cast(_Left[TC, TB], em0)

    result = map_(cast(TA, em0.value))
    if not isinstance(result, Either):
        raise ArgumentTypeError("Bind should return Either")

    return result


def then(em0: Either[TC, TA], em1: Either[TC, TB]) -> Either[TC, TB]:
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


def if_left(em0: Either[TA, TB], lft: TB) -> TB:
    return either(lambda _: lft, __id, em0)


def if_right(em0: Either[TA, TB], rgt: TA) -> TA:
    return either(__id, lambda _: rgt, em0)


def is_left(em0: Either[TA, TB]) -> bool:
    return isinstance(em0, _Left)


def is_right(em0: Either[TA, TB]) -> bool:
    return not is_left(em0)


def left(value: TA) -> Either[TA, TB]:
    return _Left(value)


def lefts(eithers: List[Either[TA, TB]]) -> List[TA]:
    return list(map(lambda either: cast(TA, either.value), filter(is_left, eithers)))


def rights(eithers: List[Either[TA, TB]]) -> List[TB]:
    return list(map(lambda either: cast(TB, either.value), filter(is_right, eithers)))


def right(value: TB) -> Either[TA, TB]:
    return pure(value)


pure = _Right  # pylint: disable=invalid-name

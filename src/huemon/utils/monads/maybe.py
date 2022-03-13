# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

from argparse import ArgumentTypeError
from typing import Callable, Generic, TypeVar

TA = TypeVar("TA")
TB = TypeVar("TB")


class Maybe(Generic[TA]):  # pylint: disable=too-few-public-methods
    value: TA

    def bind(self, map_: Callable[[TA], Maybe[TB]]) -> Maybe[TB]:
        return bind(self, map_)

    def fmap(self, map_: Callable[[TA], TB]) -> Maybe[TB]:
        return fmap(self, map_)

    def is_nothing(self) -> bool:
        return is_nothing(self)

    @staticmethod
    def of(value: TA):  # pylint: disable=invalid-name
        return of(value)

    def maybe(self: Maybe[TA], fallback: TB, map_: Callable[[TA], TB]) -> TB:
        return maybe(fallback, map_, self)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Maybe):
            return False

        if __o.is_nothing() or self.is_nothing():
            return __o.is_nothing() and self.is_nothing()

        return __o.value == self.value


class Just(Maybe[TA]):  # pylint: disable=too-few-public-methods
    value: TA

    def __init__(self, value: TA):
        self.value = value

    def __str__(self) -> str:
        return f"Just(value={self.value.__str__()})"


class Nothing(Maybe[TA]):  # pylint: disable=too-few-public-methods
    def __str__(self) -> str:
        return "Nothing"


nothing: Maybe = Nothing()

pure = Just  # pylint: disable=invalid-name


def bind(em0: Maybe[TA], map_: Callable[[TA], Maybe[TB]]) -> Maybe[TB]:
    if is_nothing(em0):
        return nothing

    result = map_(em0.value)
    if not isinstance(result, Maybe):
        raise ArgumentTypeError("Bind should return Maybe")

    return result


def fmap(em0: Maybe[TA], map_: Callable[[TA], TB]) -> Maybe[TB]:
    return bind(em0, lambda m0: pure(map_(m0)))


def is_nothing(em0: Maybe[TA]) -> bool:
    return isinstance(em0, Nothing)


def maybe(fallback: TB, map_: Callable[[TA], TB], em0: Maybe[TA]) -> TB:
    return fallback if is_nothing(em0) else map_(em0.value)


def of(value: TA):  # pylint: disable=invalid-name
    return nothing if not value else pure(value)

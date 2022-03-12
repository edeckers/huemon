# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from typing import Callable, Generic, TypeVar

TA = TypeVar("TA")
TB = TypeVar("TB")


class Maybe(Generic[TA]):  # pylint: disable=too-few-public-methods
    value = None


class Just(Maybe[TA]):  # pylint: disable=too-few-public-methods
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return f"Just(value={self.value.__str__()})"


class Nothing(Maybe[TA]):  # pylint: disable=too-few-public-methods
    def __init__(self):
        self.value = None

    def __str__(self) -> str:
        return "Nothing"


nothing = Nothing()


def bind(em0: Maybe[TA], map_: Callable[[TA], Maybe[TB]]) -> Maybe[TB]:
    return nothing if is_nothing(em0) else map_(em0.value)


def flat_map(em0: Maybe[TA], map_: Callable[[TA], TB]) -> Maybe[TB]:
    return bind(em0, lambda m0: pure(map_(m0.value)))


def is_nothing(em0: Maybe[TA]) -> bool:
    return em0 == nothing


def maybe(fallback: TB, map_: Callable[[TA], TB], em0: Maybe[TA]) -> TB:
    return fallback if is_nothing(em0) else map_(em0.value)


def mb_of(value: TA):
    return nothing if not value else pure(value)


def pure(value: TA):
    return Just(value)

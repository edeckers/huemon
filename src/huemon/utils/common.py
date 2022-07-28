from typing import Sequence, TypeVar

TS = TypeVar("TS")


def fst(seq: Sequence[TS]) -> TS:
    return seq[0]


def snd(seq: Sequence[TS]) -> TS:
    return seq[1]

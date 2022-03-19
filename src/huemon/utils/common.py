from typing import Sequence, TypeVar

TA = TypeVar("TA")


def fst(seq: Sequence[TA]) -> TA:
    return seq[0]


def snd(seq: Sequence[TA]) -> TA:
    return seq[1]

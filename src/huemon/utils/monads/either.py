# Written by Alex Euler (unlicensed)
# source: https://github.com/alexeuler/monad/blob/master/python/src/either.py

from huemon.utils.monads.monad import Monad


class Either(Monad):
    is_left = None
    value = None

    # pure :: a -> Either a
    @staticmethod
    def pure(value):
        return Right(value)

    # flat_map :: # Either a -> (a -> Either b) -> Either b
    def flat_map(self, map_function):
        return self if self.is_left else map_function(self.value)


class Left(Either):
    def __init__(self, value):
        self.value = value
        self.is_left = True


class Right(Either):
    def __init__(self, value):
        self.value = value
        self.is_left = False

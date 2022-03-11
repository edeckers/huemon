# Written by Alex Euler (unlicensed)
# source: https://github.com/alexeuler/monad/blob/master/python/src/option.py

from huemon.utils.monads.monad import Monad


class Maybe(Monad):
    defined = None
    value = None

    # pure :: a -> Maybe a
    @staticmethod
    def pure(value):
        return Just(value)

    # flat_map :: # Maybe a -> (a -> Maybe b) -> Maybe b
    def flat_map(self, map_function):
        return map_function(self.value) if self.defined else nil


class Just(Maybe):
    def __init__(self, value):
        self.value = value
        self.defined = True


class Nil(Maybe):
    def __init__(self):
        self.value = None
        self.defined = False


nil = Nil()

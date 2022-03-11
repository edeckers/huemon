# Written by Alex Euler (unlicensed)
# source: https://github.com/alexeuler/monad/blob/master/python/src/monad.py
class Monad:
    # pure :: a -> M a
    @staticmethod
    def pure(value):
        raise Exception("pure method needs to be implemented")

    # flat_map :: # M a -> (a -> M b) -> M b
    def flat_map(self, map_function):  # pylint: disable=no-self-use
        raise Exception("flat_map method needs to be implemented")

    # map :: # M a -> (a -> b) -> M b
    def map(self, map_function):
        return self.flat_map(lambda x: self.pure(map_function(x)))

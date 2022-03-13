# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import unittest
from argparse import ArgumentTypeError

from huemon.utils.monads.either import left, lefts, pure, right, rights


class TestMonadeither(unittest.TestCase):
    def test_when_fmap_on_left_return_left(self):
        left_value = left("")
        mapped_value = left_value.fmap(lambda _: "")

        self.assertEqual(left_value, mapped_value, "Left.fmap should result in Left")

    def test_when_fmap_on_right_return_right(self):
        int_value = 42
        mapper = lambda value: value * 2
        either_int = pure(int_value).fmap(mapper)

        self.assertEqual(
            pure(mapper(int_value)), either_int, "Right.fmap should result in Right"
        )

    def test_when_bind_on_right_return_either(self):
        int_value = 42

        either_int = pure(int_value)

        either_left = pure(int_value).bind(lambda _: left(0))

        mapper = lambda value: pure(value * 2)
        either_right = either_int.bind(mapper)

        with self.assertRaises(ArgumentTypeError):
            pure(1).bind(lambda _: "Some none either-type")

        self.assertEqual(left(0), either_left, "Right.bind should result in Either")

        self.assertEqual(
            mapper(int_value), either_right, "Right.bind should result in Either"
        )

    def test_when_either_use_designated_left_and_right_maps(self):
        int_value = 42

        mapper_left = lambda value: value * 2
        mapper_right = lambda value: value * 4

        result_left = left(int_value).either(mapper_left, mapper_right)
        result_right = right(int_value).either(mapper_left, mapper_right)

        self.assertEqual(
            mapper_left(int_value),
            result_left,
            "Left.either should return left-mapped value",
        )
        self.assertEqual(
            mapper_right(int_value),
            result_right,
            "Right.either should return right-mapped value",
        )

    def test_when_list_map_filter_correct_types(self):
        left_values = [0, 2, 4]
        right_values = [1, 3, 5]

        eithers = list(map(left, left_values)) + list(map(right, right_values))

        self.assertEqual(
            left_values,
            lefts(eithers),
            "lefts should return Left values only",
        )
        self.assertEqual(
            right_values,
            rights(eithers),
            "rights should return Right values only",
        )

    def test_when_left_chain_should_not_do_anything(self):
        either_left = left(0)
        either_right = right(0)

        result = either_left.chain(either_right)

        self.assertEqual(
            either_left,
            result,
            "Chaining left should not do anything",
        )

    def test_when_right_chain_should_return_chained_monad(self):
        either_right_0 = right(21)
        either_right_1 = right(42)

        result = either_right_0.chain(either_right_1)

        self.assertEqual(
            either_right_1,
            result,
            "Chaining right should return second Either",
        )

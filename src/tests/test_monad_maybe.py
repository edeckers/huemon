# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import unittest
from argparse import ArgumentTypeError

from huemon.utils.monads.maybe import Maybe, nothing, pure


class TestMonadMaybe(unittest.TestCase):
    def test_when_of_is_empty_return_nothing(self):
        maybe_none = Maybe.of(None)
        maybe_false = Maybe.of(False)
        maybe_zero = Maybe.of(0)
        maybe_empty_str = Maybe.of("")
        maybe_empty_obj = Maybe.of({})
        maybe_empty_list = Maybe.of([])

        self.assertEqual(nothing, maybe_none, "None should result in Nothing")
        self.assertEqual(nothing, maybe_false, "False should result in Nothing")
        self.assertEqual(nothing, maybe_zero, "Zero should result in Nothing")
        self.assertEqual(
            nothing, maybe_empty_str, "Empty string should result in Nothing"
        )
        self.assertEqual(
            nothing, maybe_empty_obj, "Empty object should result in Nothing"
        )
        self.assertEqual(
            nothing, maybe_empty_list, "Empty list should result in Nothing"
        )
        self.assertTrue(
            nothing.is_nothing(), "Nothing should return True on is_nothing"
        )

    def test_when_of_is_not_empty_return_just(self):
        int_val = 1
        str_val = "some value"
        obj_val = {"some_field": "some value"}
        list_val = ["some value"]

        maybe_true = Maybe.of(True)
        maybe_int = Maybe.of(int_val)
        maybe_str = Maybe.of(str_val)
        maybe_obj = Maybe.of(obj_val)
        maybe_list = Maybe.of(list_val)

        self.assertEqual(pure(True), maybe_true, "True should result in Just")
        self.assertFalse(
            maybe_true.is_nothing(), "True should return False on is_nothing"
        )
        self.assertEqual(pure(int_val), maybe_int, "Int should result in Just")
        self.assertFalse(
            maybe_int.is_nothing(), "Just should return False on is_nothing"
        )
        self.assertEqual(pure(str_val), maybe_str, "String should result in Just")
        self.assertFalse(
            maybe_str.is_nothing(), "Just should return False on is_nothing"
        )
        self.assertEqual(pure(obj_val), maybe_obj, "Object should result in Just")
        self.assertFalse(
            maybe_obj.is_nothing(), "Just should return False on is_nothing"
        )
        self.assertEqual(pure(list_val), maybe_list, "List should result in Just")
        self.assertFalse(
            maybe_list.is_nothing(), "Just should return False on is_nothing"
        )

    def test_when_fmap_on_nothing_return_nothing(self):
        maybe_nothing = nothing.fmap(lambda _: "")

        self.assertEqual(
            nothing, maybe_nothing, "Nothing.fmap should result in Nothing"
        )

    def test_when_fmap_on_just_return_just(self):
        maybe_int = pure(1).fmap(lambda value: value + 1)

        self.assertEqual(pure(2), maybe_int, "Just.fmap should result in Just")

    def test_when_bind_on_just_return_maybe(self):
        maybe_nothing = pure(1).bind(lambda _: nothing)
        maybe_int = pure(1).bind(lambda value: pure(value + 1))

        with self.assertRaises(ArgumentTypeError):
            pure(1).bind(lambda _: "Some none Maybe-type")

        self.assertEqual(nothing, maybe_nothing, "Just.bind should result in Maybe")
        self.assertEqual(pure(2), maybe_int, "Just.bind should result in Maybe")

    def test_when_maybe_on_nothing_return_fallback(self):
        mapper = lambda value: value * 2
        fallback_value = 42
        result = nothing.maybe(fallback_value, mapper)

        self.assertEqual(fallback_value, result, "Nothing.maybe should return fallback")

    def test_when_maybe_on_just_return_mapped_value(self):
        int_value = 1

        mapper = lambda value: value * 2
        result = pure(int_value).maybe(42, mapper)

        self.assertEqual(
            mapper(int_value), result, "Just.maybe should return mapped value"
        )

# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import unittest

from huemon.api.api import Api
from huemon.api.api_factory import create_api, create_hue_hub_url
from huemon.api.cached_api import CachedApi


class TestApiConfiguration(unittest.TestCase):
    def test_when_no_api_configuration_available_throw(self):
        with self.assertRaises(Exception):
            create_hue_hub_url({})

    def test_when_cache_enabled_return_cached(self):
        api = create_api(
            {"ip": "IRRELEVANT_IP", "key": "IRRELEVANT_KEY", "cache": {"enable": True}}
        )

        self.assertIsInstance(api, CachedApi)

    def test_when_cache_enabled_return_regular(self):
        api = create_api(
            {"ip": "IRRELEVANT_IP", "key": "IRRELEVANT_KEY", "cache": {"enable": False}}
        )

        self.assertNotIsInstance(api, CachedApi)
        self.assertIsInstance(api, Api)

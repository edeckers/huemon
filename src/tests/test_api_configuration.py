# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import os
import tempfile
import threading
import unittest

from huemon.api.api import Api
from huemon.api.api_factory import create_api, create_hue_hub_url
from huemon.api.cached_api import CachedApi
from huemon.util import run_locked


class TestApiConfiguration(unittest.TestCase):
    def test_when_no_api_configuration_available_throw(self):
        with self.assertRaises(Exception):
            create_hue_hub_url({})

    def test_when_cache_enabled_return_cached(self):
        api = create_api(
            {"ip": "IRRELEVANT_IP", "key": "IRRELEVANT_KEY", "cache": {"enable": True}}
        )

        self.assertIsInstance(api, CachedApi)

    def test_when_cache_disabled_return_regular(self):
        api = create_api(
            {"ip": "IRRELEVANT_IP", "key": "IRRELEVANT_KEY", "cache": {"enable": False}}
        )

        self.assertNotIsInstance(api, CachedApi)
        self.assertIsInstance(api, Api)

    @staticmethod
    def __wait(mutex: threading.Lock, is_started: threading.Event):
        is_started.set()

        with mutex:
            pass

    def test_when_locked_return_none(self):
        (lfd, lock_file_path) = tempfile.mkstemp()

        mutex = threading.Lock()

        with mutex:
            is_started_event = threading.Event()
            target = lambda: run_locked(
                lock_file_path,
                lambda: TestApiConfiguration.__wait(mutex, is_started_event),
            )

            thread0 = threading.Thread(target=target)

            thread0.start()
            is_started_event.wait()

            maybe_true = run_locked(lock_file_path, lambda: True)

        thread0.join(5)

        os.close(lfd)

        self.assertIsNone(maybe_true)

    def test_when_locked_raises_exception_return_none(self):
        (lfd, lock_file_path) = tempfile.mkstemp()

        raise_exception = lambda: 1 / 0

        maybe_true = run_locked(lock_file_path, raise_exception)

        os.close(lfd)

        self.assertIsNone(maybe_true)

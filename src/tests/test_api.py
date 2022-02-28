import tempfile
from typing import List
import unittest

from huemon.api.cached_api import CachedApi
from huemon.api_interface import ApiInterface
from tests.fixtures import FIELD_SYSTEM_SWVERSION, MutableApi, create_system_config


CACHE_VALIDITY_INFINITE_SECONDS = 1_000_000
CACHE_VALIDITY_ZERO_SECONDS = 0


class TestCachedApi(unittest.TestCase):
  def test_when_cache_not_expired_return_cache(self):
    mutable_api = MutableApi()

    system_config_pre = create_system_config()
    version_pre = system_config_pre[FIELD_SYSTEM_SWVERSION]

    mutable_api.set_system_config(system_config_pre)

    api = CachedApi(
        mutable_api,
        CACHE_VALIDITY_INFINITE_SECONDS,
        tempfile.mkdtemp())

    system_config_pre_recv = api.get_system_config()
    version_pre_recv = system_config_pre_recv[FIELD_SYSTEM_SWVERSION]

    system_config_post = create_system_config()
    version_post = system_config_post[FIELD_SYSTEM_SWVERSION]
    mutable_api.set_system_config(system_config_post)

    system_config_post_recv = api.get_system_config()
    version_post_recv = system_config_post_recv[FIELD_SYSTEM_SWVERSION]

    self.assertEqual(
        version_pre,
        version_pre_recv,
        "Received version should equal set version")
    self.assertEqual(
        version_pre_recv,
        version_post_recv,
        "Received version before and after mutation should be the same")
    self.assertNotEqual(
        version_pre,
        version_post,
        "Set versions should differ")

  def test_when_cache_expired_return_new_data(self):
    mutable_api = MutableApi()

    system_config_pre = create_system_config()
    version_pre = system_config_pre[FIELD_SYSTEM_SWVERSION]

    mutable_api.set_system_config(system_config_pre)

    api = CachedApi(
        mutable_api,
        CACHE_VALIDITY_ZERO_SECONDS,
        tempfile.mkdtemp())

    system_config_pre_recv = api.get_system_config()
    version_pre_recv = system_config_pre_recv[FIELD_SYSTEM_SWVERSION]

    system_config_post = create_system_config()
    version_post = system_config_post[FIELD_SYSTEM_SWVERSION]
    mutable_api.set_system_config(system_config_post)

    system_config_post_recv = api.get_system_config()
    version_post_recv = system_config_post_recv[FIELD_SYSTEM_SWVERSION]

    self.assertEqual(
        version_pre,
        version_pre_recv,
        "Received version should equal set version")
    self.assertEqual(
        version_post,
        version_post_recv,
        "Received version should equal set version")
    self.assertNotEqual(
        version_pre_recv,
        version_post_recv,
        "Received version before and after mutation should differ")
    self.assertNotEqual(
        version_pre,
        version_post,
        "Set versions should differ")

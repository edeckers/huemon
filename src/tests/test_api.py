import tempfile
import time
from typing import List
import unittest

from huemon.api.cached_api import CachedApi
from huemon.api_interface import ApiInterface
from tests.fixtures import FIELD_SYSTEM_VERSION, create_system_config


CACHE_VALIDITY_INFINITE_SECONDS = 1_000_000
CACHE_VALIDITY_ZERO_SECONDS = 0


class MutableApi(ApiInterface):
  def set_system_config(self, json_data: dict):
    self.system_config = json_data

  def set_lights(self, json_data: List[dict]):
    self.lights = json_data

  def set_sensors(self, json_data: List[dict]):
    self.sensors = json_data

  def get_system_config(self):
    return self.system_config

  def get_lights(self):
    return self.lights

  def get_sensors(self):
    return self.sensors


class TestCachedApi(unittest.TestCase):
  def test_when_cache_not_expired_return_cache(self):
    mutable_api = MutableApi()

    system_config_pre = create_system_config()
    version_pre = system_config_pre[FIELD_SYSTEM_VERSION]

    mutable_api.set_system_config(system_config_pre)

    api = CachedApi(
        mutable_api,
        CACHE_VALIDITY_INFINITE_SECONDS,
        tempfile.mkdtemp())

    system_config_pre_recv = api.get_system_config()
    version_pre_recv = system_config_pre_recv[FIELD_SYSTEM_VERSION]

    system_config_post = create_system_config()
    version_post = system_config_post[FIELD_SYSTEM_VERSION]
    mutable_api.set_system_config(system_config_post)

    system_config_post_recv = api.get_system_config()
    version_post_recv = system_config_post_recv[FIELD_SYSTEM_VERSION]

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
    version_pre = system_config_pre[FIELD_SYSTEM_VERSION]

    mutable_api.set_system_config(system_config_pre)

    api = CachedApi(
        mutable_api,
        CACHE_VALIDITY_ZERO_SECONDS,
        tempfile.mkdtemp())

    system_config_pre_recv = api.get_system_config()
    version_pre_recv = system_config_pre_recv[FIELD_SYSTEM_VERSION]

    system_config_post = create_system_config()
    version_post = system_config_post[FIELD_SYSTEM_VERSION]
    mutable_api.set_system_config(system_config_post)

    system_config_post_recv = api.get_system_config()
    version_post_recv = system_config_post_recv[FIELD_SYSTEM_VERSION]

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

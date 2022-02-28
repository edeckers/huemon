# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from fcntl import LOCK_EX, LOCK_NB, flock
import json
import os
from os.path import exists
import tempfile
import time
from huemon.api.api_interface import ApiInterface
from huemon.infrastructure.logger_factory import create_logger

LOG = create_logger()

DEFAULT_MAX_CACHE_AGE_SECONDS = 10
DEFAULT_CACHE_PATH = tempfile.gettempdir()


class CachedApi(ApiInterface):
  def __init__(self, api: ApiInterface, max_cache_age_seconds=DEFAULT_MAX_CACHE_AGE_SECONDS, cache_path=DEFAULT_CACHE_PATH):
    self.api = api
    self.cache_path = cache_path
    self.max_cache_age_seconds = max_cache_age_seconds

  def __tf(self, filename):
    return "/".join([self.cache_path, filename])

  def __cache(self, resource_type: str, fn_call):
    temp_filename = f"zabbix-hue.{resource_type}"
    cache_file_path = self.__tf(f"{temp_filename}.json")
    lock_file = self.__tf(f"{temp_filename}.lock")

    does_cache_file_exist = exists(cache_file_path)
    cache_age_seconds = time.time(
    ) - os.path.getmtime(cache_file_path) if does_cache_file_exist else 0
    is_cache_file_expired = not does_cache_file_exist or cache_age_seconds >= self.max_cache_age_seconds
    is_cache_hit = not is_cache_file_expired

    if is_cache_hit:
      with open(cache_file_path, "r") as f_json:
        LOG.debug("Cache hit (type=%s,age_seconds=%s,max_cache_age_seconds=%s)",
                  resource_type, round(cache_age_seconds, 1), self.max_cache_age_seconds)
        return json.loads(f_json.read())

    with open(lock_file, "w") as f_lock:
      try:
        flock(f_lock.fileno(), LOCK_EX | LOCK_NB)
        LOG.debug("Acquired lock successfully (file=%s)", lock_file)

        tmp_fd, tmp_file_path = tempfile.mkstemp()
        with open(tmp_file_path, "w") as f_tmp:
          f_tmp.write(json.dumps(fn_call()))

        os.close(tmp_fd)

        os.rename(tmp_file_path, cache_file_path)

        with open(cache_file_path) as f_json:
          return json.loads(f_json.read())
      except:  # pylint: disable=bare-except
        LOG.debug("Failed to acquire lock, cache hit (file=%s)", lock_file)

    if not does_cache_file_exist:
      return []

    with open(cache_file_path) as f_json:
      return json.loads(f_json.read())

  def get_system_config(self):
    return self.__cache("system", self.api.get_system_config)

  def get_lights(self):
    return self.__cache("lights", self.api.get_lights)

  def get_sensors(self):
    return self.__cache("sensors", self.api.get_sensors)

  def get_batteries(self):
    return self.__cache("batteries", self.api.get_batteries)

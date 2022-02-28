import time


FIELD_SYSTEM_VERSION = "version"
FIELD_SYSTEM_IS_UPDATE_AVAILABLE = "is_update_available"


def __generate_version():
  return str(time.process_time())


def create_system_config(version: str = None, is_update_available: bool = False):
  return {
      FIELD_SYSTEM_VERSION: version if version else __generate_version(),
      FIELD_SYSTEM_IS_UPDATE_AVAILABLE: int(is_update_available)
  }

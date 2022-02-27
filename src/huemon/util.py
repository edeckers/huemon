import os
from pathlib import Path


def create_local_path(relative_path: str):
  return str(os.path.join(
      Path(__file__).parent.absolute(), relative_path))


DEFAULT_COMMANDS_AVAILABLE_PATH = create_local_path("commands_available")
DEFAULT_COMMANDS_ENABLED_PATH = create_local_path("commands_enabled")
DEFAULT_DISCOVERIES_AVAILABLE_PATH = create_local_path("discoveries_available")
DEFAULT_DISCOVERIES_ENABLED_PATH = create_local_path("discoveries_enabled")

PLUGIN_TYPE_MAPPING = {
    "commands": {
        "available": DEFAULT_COMMANDS_AVAILABLE_PATH,
        "enabled": DEFAULT_COMMANDS_ENABLED_PATH,
    },
    "discoveries": {
        "available": DEFAULT_DISCOVERIES_AVAILABLE_PATH,
        "enabled": DEFAULT_DISCOVERIES_ENABLED_PATH,
    },
}


def __create_plugins_path(plugin_type: str, config: dict, path_type: str, fallback_path: str = None):
  return config[plugin_type][path_type] if \
      plugin_type in config and path_type in config[plugin_type] else \
      (fallback_path or PLUGIN_TYPE_MAPPING[plugin_type][path_type])


def get_commands_path(config: dict, path_type: str, fallback_path: str = None):
  return __create_plugins_path("commands", config, path_type, fallback_path)


def get_discoveries_path(config: dict, path_type: str, fallback_path: str = None):
  return __create_plugins_path("discoveries", config, path_type, fallback_path)
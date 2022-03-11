# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.


def __create_plugins_path(plugin_type: str, config: dict, fallback_path: str = None):
    plugins_section_exists = "plugins" in config
    if not plugins_section_exists:
        return fallback_path

    plugin_type_exists = config["plugins"][plugin_type]
    if not plugin_type_exists:
        return fallback_path

    return (
        config["plugins"][plugin_type]["path"]
        if "path" in config["plugins"][plugin_type]
        else fallback_path
    )


def get_command_plugins_path(config: dict, fallback_path: str = None):
    return __create_plugins_path("commands", config, fallback_path)


def get_discovery_plugins_path(config: dict, fallback_path: str = None):
    return __create_plugins_path("discoveries", config, fallback_path)

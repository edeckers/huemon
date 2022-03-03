# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import importlib.util
import inspect
from pathlib import Path


def __get_plugin_type(module_name: str, path: str, sub_class):
    maybe_spec = importlib.util.spec_from_file_location(module_name, path)
    if not maybe_spec:
        return None

    module = importlib.util.module_from_spec(maybe_spec)

    if not maybe_spec.loader:
        return None

    maybe_spec.loader.exec_module(module)

    plugin_types = list(
        filter(
            lambda m: inspect.isclass(m[1])
            and issubclass(m[1], sub_class)
            and m[1] is not sub_class,
            inspect.getmembers(module),
        )
    )

    if len(plugin_types) == 0:
        return None

    _, hue_command_class = plugin_types[0]

    return hue_command_class


def load_plugins(module_name: str, path: str, plugin_type):
    return list(
        map(
            lambda p: __get_plugin_type(
                f"{module_name}.{p.stem}", str(p.absolute()), plugin_type
            ),
            Path(path).glob("*.py"),
        )
    )

# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import importlib.util
import inspect
from importlib.machinery import ModuleSpec
from pathlib import Path
from types import ModuleType
from typing import Tuple

from huemon.utils.monads.either import Either, Left, Right, bind, chain, flat_map, pure
from huemon.utils.monads.maybe import maybe, mb_of


def __get_plugin_type(module_name: str, path: str, sub_class) -> Either[str, object]:
    error_or_module_spec = maybe(
        Left[str, ModuleSpec]("ModuleSpec could not be loaded from the provided path"),
        Right[str, ModuleSpec],
        mb_of(importlib.util.spec_from_file_location(module_name, path)),
    )

    error_or_spec_loader = bind(
        error_or_module_spec,
        lambda spec: Left[str, ModuleSpec]("ModuleSpec has no loader")
        if not spec.loader
        else Right[str, ModuleSpec](spec),
    )

    error_or_spec_and_module = bind(
        error_or_spec_loader,
        lambda spec: maybe(
            Left[str, Tuple[ModuleSpec, ModuleType]](
                "Module could not be loaded from ModuleSpec"
            ),
            lambda module: Right[str, Tuple[ModuleSpec, ModuleType]]((spec, module)),
            mb_of(importlib.util.module_from_spec(spec)),
        ),
    )

    error_or_module = chain(
        bind(
            error_or_spec_and_module, lambda sm: pure(sm[0].loader.exec_module(sm[1]))
        ),
        flat_map(error_or_spec_and_module, lambda sm: sm[1]),
    )

    error_or_plugin_types = flat_map(
        error_or_module,
        lambda module: list(
            filter(
                lambda member: inspect.isclass(member[1])
                and issubclass(member[1], sub_class)
                and member[1] is not sub_class,
                inspect.getmembers(module),
            )
        ),
    )

    return bind(
        error_or_plugin_types,
        lambda plugin_types: pure(plugin_types[0][1])
        if len(plugin_types) > 0
        else Left(f"No plugin of type `{sub_class}` found"),
    )


def load_plugins(module_name: str, path: str, plugin_type):
    return list(
        map(
            lambda p: __get_plugin_type(
                f"{module_name}.{p.stem}", str(p.absolute()), plugin_type
            ),
            Path(path).glob("*.py"),
        )
    )

# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import importlib.util
import inspect
from importlib.machinery import ModuleSpec
from pathlib import Path
from types import ModuleType
from typing import List, Tuple, Type, TypeVar

from huemon.utils.monads.either import Either, Left, Right, bind, chain
from huemon.utils.monads.either import fmap as e_fmap
from huemon.utils.monads.either import left
from huemon.utils.monads.either import pure as e_pure
from huemon.utils.monads.either import right
from huemon.utils.monads.maybe import maybe
from huemon.utils.monads.maybe import of as m_of

TA = TypeVar("TA")


def __get_plugin_type(
    module_name: str, path: str, sub_class: Type[TA]
) -> Either[str, Type[TA]]:
    error_or_module_spec: Either[str, ModuleSpec] = maybe(
        left("ModuleSpec could not be loaded from the provided path"),
        right,
        m_of(importlib.util.spec_from_file_location(module_name, path)),
    )

    error_or_spec_loader = bind(
        error_or_module_spec,
        lambda spec: Left[str, ModuleSpec]("ModuleSpec has no loader")
        if not spec.loader
        else Right[str, ModuleSpec](spec),
    )

    error_or_spec_and_module: Either[str, Tuple[ModuleSpec, ModuleType]] = bind(
        error_or_spec_loader,
        lambda spec: maybe(
            left("Module could not be loaded from ModuleSpec"),
            lambda module: right((spec, module)),
            m_of(importlib.util.module_from_spec(spec)),
        ),
    )

    error_or_module = chain(
        bind(
            error_or_spec_and_module,
            lambda sm: e_pure(
                m_of(sm[0].loader).fmap(lambda loader: loader.exec_module(sm[1]))
            ),
        ),
        e_fmap(error_or_spec_and_module, lambda sm: sm[1]),
    )

    error_or_plugin_types = e_fmap(
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
        lambda plugin_types: e_pure(plugin_types[0][1])
        if len(plugin_types) > 0
        else Left(f"No plugin of type `{sub_class}` found"),
    )


def load_plugins(
    module_name: str, path: str, plugin_type: Type[TA]
) -> List[Either[str, Type[TA]]]:
    return list(
        map(
            lambda plugin_path: __get_plugin_type(
                f"{module_name}.{plugin_path.stem}",
                str(plugin_path.absolute()),
                plugin_type,
            ),
            Path(path).glob("*.py"),
        )
    )

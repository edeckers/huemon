# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import importlib.util
import inspect
from pathlib import Path
from typing import List, Tuple, Type, TypeVar, cast

from huemon.utils.errors import E_CODE_PLUGIN_LOADER, HueError
from huemon.utils.monads.either import Either, Left, right
from huemon.utils.monads.maybe import Maybe

TA = TypeVar("TA")


def __error(message: str) -> HueError:
    return HueError(E_CODE_PLUGIN_LOADER, message)


def __lerror(message: str) -> Left[HueError, TA]:
    return Left[HueError, TA](__error(message))


def __get_plugin_type(
    module_name: str, path: str, sub_class: Type[TA]
) -> Either[HueError, Type[TA]]:
    return (
        Maybe.of(importlib.util.spec_from_file_location(module_name, path))
        .maybe(
            __lerror("ModuleSpec could not be loaded from the provided path"),
            right,
        )
        .bind(
            lambda spec: Maybe.of(spec.loader).maybe(
                __lerror("ModuleSpec has no loader"), lambda _: right(spec)
            )
        )
        .bind(
            lambda spec: Maybe.of(importlib.util.module_from_spec(spec)).maybe(
                __lerror("Module could not be loaded from ModuleSpec"),
                lambda module: right((spec, module)),
            ),
        )
        .discard(
            lambda sm: Either.pure(
                Maybe.of(sm[0].loader).bind(
                    lambda loader: Maybe.of(loader.exec_module(sm[1]))
                )
            )
        )
        .fmap(lambda sm: sm[1])
        .fmap(
            lambda module: list(
                map(
                    lambda obj: cast(Tuple[str, Type[TA]], obj),
                    filter(
                        lambda member: inspect.isclass(member[1])
                        and issubclass(member[1], sub_class)
                        and member[1] is not sub_class,
                        inspect.getmembers(module),
                    ),
                ),
            ),
        )
        .bind(
            lambda plugin_types: Maybe.of(len(plugin_types) > 0).maybe(
                __lerror(f"No plugin of type `{sub_class}` found"),
                lambda _: right(plugin_types[0][1]),
            )
        )
    )


def load_plugins(
    module_name: str, path: str, plugin_type: Type[TA]
) -> List[Either[HueError, Type[TA]]]:
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

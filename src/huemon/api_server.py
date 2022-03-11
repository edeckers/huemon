# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import contextlib
import io
import threading
from typing import List

from fastapi import FastAPI, HTTPException, Query, Response, status

from huemon.commands.command_handler import create_default_command_handler
from huemon.infrastructure.logger_factory import create_logger
from huemon.utils.plugins import get_command_plugins_path

LOG = create_logger()


class HuemonServerFactory:  # pylint: disable=too-few-public-methods
    __stdout_reader_mutex = threading.Lock()

    @staticmethod
    def __create_command_route_handler(command_handler, command_name: str):
        empty_query = Query([])

        def handle_command_route(
            q: List[str] = empty_query,
        ):  # pylint: disable=invalid-name
            with HuemonServerFactory.__stdout_reader_mutex:
                context_reader = io.StringIO()
                with contextlib.redirect_stdout(context_reader):
                    try:
                        command_handler.exec(command_name, q)
                    except SystemExit as system_exit:
                        raise HTTPException(
                            detail=context_reader.getvalue(),
                            status_code=status.HTTP_400_BAD_REQUEST,
                        ) from system_exit

            return Response(context_reader.getvalue(), media_type="plain/text")

        return handle_command_route

    @staticmethod
    def create(config: dict) -> FastAPI:
        app = FastAPI()

        command_handler = create_default_command_handler(
            config, get_command_plugins_path(config)
        )

        for command_name in command_handler.available_commands():
            app.add_api_route(
                f"/{command_name}",
                HuemonServerFactory.__create_command_route_handler(
                    command_handler, command_name
                ),
            )

        return app

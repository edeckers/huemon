import contextlib
import io
from typing import List

from fastapi import FastAPI, HTTPException, Query, Response, status

from huemon.commands.command_handler import create_default_command_handler
from huemon.infrastructure.config_factory import create_config
from huemon.infrastructure.logger_factory import create_logger
from huemon.util import get_commands_path

app = FastAPI()

CONFIG = create_config()
LOG = create_logger()

command_handler = create_default_command_handler(
    CONFIG, get_commands_path(CONFIG, "enabled")
)


def create_command_route_handler(command_name: str):
    empty_query = Query([])

    def handle_command_route(
        q: List[str] = empty_query,
    ):  # pylint: disable=invalid-name
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


def __init__():
    for command_name in command_handler.available_commands():
        app.add_api_route(
            f"/{command_name}", create_command_route_handler(command_name)
        )


__init__()

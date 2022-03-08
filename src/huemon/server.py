import contextlib
import io
import json

from fastapi import FastAPI, HTTPException, status

from huemon.commands.command_handler import create_default_command_handler
from huemon.infrastructure.config_factory import create_config
from huemon.infrastructure.logger_factory import create_logger
from huemon.util import get_commands_path

app = FastAPI()

CONFIG = create_config()
LOG = create_logger()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/discover")
async def discover():
    command_handler = create_default_command_handler(
        CONFIG, get_commands_path(CONFIG, "enabled")
    )

    context_reader = io.StringIO()
    with contextlib.redirect_stdout(context_reader):
        try:
            command_handler.exec("discover", ["lights"])
        except SystemExit:
            raise HTTPException(  # pylint: disable=raise-missing-from
                detail=context_reader.getvalue(),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    return json.loads(context_reader.getvalue())

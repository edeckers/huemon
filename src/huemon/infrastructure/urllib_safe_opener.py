# By Jonathan Bowman
# https://dev.to/bowmanjd/hardening-and-simplifying-python-s-urlopen-4gee dd 20220302@1410

import typing
import urllib.request

from huemon.infrastructure.logger_factory import create_logger

LOG = create_logger()


class WhitelistedSchemaOpener(urllib.request.OpenerDirector):
    def __init__(self, handlers: typing.Iterable = None):
        super().__init__()
        handlers = handlers or (
            urllib.request.UnknownHandler,
            urllib.request.HTTPHandler,
            urllib.request.HTTPDefaultErrorHandler,
            urllib.request.HTTPRedirectHandler,
            urllib.request.HTTPSHandler,
            urllib.request.HTTPErrorProcessor,
        )

        for handler_class in handlers:
            self.add_handler(handler_class())


def security_urllib_allow_http_and_https_schemas_only():
    LOG.debug("Limiting urllib.request to http and https schemas")
    urllib.request.install_opener(WhitelistedSchemaOpener())
    LOG.debug("Limited urllib.request to http and https schemas")

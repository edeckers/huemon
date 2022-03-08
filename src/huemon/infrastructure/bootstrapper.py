from huemon.infrastructure.logger_factory import create_logger
from huemon.infrastructure.urllib_safe_opener import (
    security_urllib_allow_http_and_https_schemas_only,
)

LOG = create_logger()


def bootstrap():
    LOG.debug("Bootstrapping application")
    security_urllib_allow_http_and_https_schemas_only()
    LOG.debug("Finished bootstrapping application")

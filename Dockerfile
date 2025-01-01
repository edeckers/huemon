# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

FROM python:3.8-alpine3.18

ARG HUEMON_VERSION=2.0.3

ENV HUEMON_CONFIG_PATH="/etc/huemon/config.yml"

RUN apk add bash curl

COPY src/huemon/config.example.yml ${HUEMON_CONFIG_PATH}
COPY assets/docker/entrypoint.sh /sbin/entrypoint.sh

RUN chmod +x /sbin/entrypoint.sh

COPY dist/huemon-${HUEMON_VERSION}-py3-none-any.whl /tmp

# Fixes "Cargo not installed" error: exact version is not important, as long as it
# includes the required musl wheels
# https://github.com/pydantic/pydantic/discussions/4230#discussioncomment-3163410
RUN pip install pydantic==1.10.12

RUN pip install /tmp/huemon-${HUEMON_VERSION}-py3-none-any.whl

LABEL \
    maintainer="noreply@nonono.com" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.name=huemon \
    org.label-schema.vendor=edeckers \
    org.label-schema.url="https://github.com/edeckers/huemon" \
    org.label-schema.vcs-url="https://github.com/edeckers/huemon.git"

VOLUME ["/etc/huemon", "/opt/huemon", "/var/log/huemon"]

ENTRYPOINT [ "/sbin/entrypoint.sh" ]

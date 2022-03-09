# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

FROM python:3.8-alpine3.15

ARG HUEMON_VERSION=0.6.0  

ENV HUEMON_CONFIG_PATH="/etc/huemon/config.yml"

COPY docker/entrypoint.sh /sbin/entrypoint.sh
RUN chmod 755 /sbin/entrypoint.sh

RUN apk add bash curl

RUN curl -L https://github.com/edeckers/huemon/releases/download/v${HUEMON_VERSION}/huemon-${HUEMON_VERSION}.tar.gz > /tmp/huemon.tar.gz

COPY src/huemon/config.example.yml ${HUEMON_CONFIG_PATH}

RUN /sbin/entrypoint.sh install

LABEL \
    maintainer="noreply@nonono.com" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.name=huemon \
    org.label-schema.vendor=edeckers \
    org.label-schema.url="https://github.com/edeckers/huemon" \
    org.label-schema.vcs-url="https://github.com/edeckers/huemon.git"

VOLUME ["/etc/huemon", "/opt/huemon", "/var/log/huemon"]

ENTRYPOINT [ "/sbin/entrypoint.sh" ]

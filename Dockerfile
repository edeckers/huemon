FROM python:3.8-alpine3.15

ENV HUEMON_CONFIG_DIR="/etc/huemon" \
    HUEMON_COMMANDS_ENABLED_DIR="/opt/huemon/commands_enabled" \
    HUEMON_DISCOVERIES_ENABLED_DIR="/opt/huemon/discoveries_enabled" \
    HUEMON_LOG_DIR="/var/log/huemon" \
    HUEMON_VERSION=0.0.3  

ENV HUEMON_CONFIG_PATH="${HUEMON_CONFIG_DIR}/config.yml"

COPY docker/entrypoint.sh /sbin/entrypoint.sh
RUN chmod 755 /sbin/entrypoint.sh

RUN apk add bash curl

RUN curl -L https://github.com/edeckers/huemon/releases/download/v${HUEMON_VERSION}/huemon-${HUEMON_VERSION}.tar.gz > /tmp/huemon.tar.gz
RUN pip3 install /tmp/huemon.tar.gz

COPY src/huemon/config.example.yml ${HUEMON_CONFIG_PATH}

RUN /sbin/entrypoint.sh app:install

LABEL \
    maintainer="noreply@nonono.com" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.name=huemon \
    org.label-schema.vendor=edeckers \
    org.label-schema.url="https://github.com/edeckers/huemon" \
    org.label-schema.vcs-url="https://github.com/edeckers/huemon.git"

VOLUME ["${HUEMON_CONFIG_DIR}", "${HUEMON_COMMANDS_ENABLED_DIR}", "${HUEMON_DISCOVERIES_ENABLED_DIR}", "${HUEMON_LOG_DIR}"]

ENTRYPOINT ["/sbin/entrypoint.sh"]

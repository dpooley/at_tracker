FROM python:3.8-slim

ENV INSTALL_DIR="/at_tracker" \
    BUILD_DEPS="build-essential"

RUN apt-get update \
    && groupadd -r at_tracker && useradd -m -l -r -g at_tracker at_tracker \
    && apt-get install -y ${BUILD_DEPS}

COPY ./at_tracker/ ${INSTALL_DIR}/

RUN pip3 install ${INSTALL_DIR} \
    && apt-get purge -y ${BUILD_DEPS} \
    && rm -rf /var/cache/apt/* ${INSTALL_DIR}

USER at_tracker

WORKDIR /home/at_tracker

ENTRYPOINT ["entrypoint"]

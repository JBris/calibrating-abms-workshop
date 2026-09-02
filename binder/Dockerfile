FROM ghcr.io/jbris/caliagent:1.0.0

ARG NB_USER=jovyan

ARG NB_UID=1000

ENV USER ${NB_USER}

ENV NB_UID ${NB_UID}

ENV HOME /home/${NB_USER}

ENV VIRTUAL_ENV=${HOME}/.venv \
    PATH="${HOME}/.venv/bin:$PATH"

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER} \
    && mv /workspace/* ${HOME} \
    && mv /workspace/.venv ${HOME}/.venv \
    && chown -R ${NB_UID} ${HOME}

USER ${NB_USER}

WORKDIR ${HOME}

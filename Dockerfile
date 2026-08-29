FROM python:3.11.14-bookworm AS base

ARG BUILD_DATE

ARG CALIAGENT_VERSION

LABEL maintainer=J.Bristow2@massey.ac.nz

LABEL org.label-schema.build-date=$BUILD_DATE

LABEL version=$CALIAGENT_VERSION

WORKDIR /workspace

COPY README.md README.md

COPY caliagent caliagent

COPY docs/source/workshop /workspace/workshop

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential graphviz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/downloaded_packages

FROM base AS builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock ./

RUN curl -sSL https://install.python-poetry.org | python3 -\
    && poetry install --with dev,docs \
    && rm -rf $POETRY_CACHE_DIR \
    && curl -sSL https://install.python-poetry.org | python3 - --uninstall

FROM base AS runtime

ENV VIRTUAL_ENV=/workspace/.venv \
    PATH="/workspace/.venv/bin:$PATH"

EXPOSE 8888

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

RUN chmod -R 755 /workspace

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]

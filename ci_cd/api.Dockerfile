FROM python:3.11.13-bookworm@sha256:ca0b6467f5accb0c39c154a5e242df36348d9afb009a58b4263755d78728a21c AS builder
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV="/venv" \
    PATH="/venv/bin:${PATH}"
RUN python -m pip install uv && \
    python -m venv ${VIRTUAL_ENV} && \
    uv pip install --upgrade pip setuptools wheel
COPY ./src/wh_control/pyproject.toml pyproject.toml
RUN uv pip install .

FROM python:3.11.13-bookworm@sha256:ca0b6467f5accb0c39c154a5e242df36348d9afb009a58b4263755d78728a21c
ENV PYTHONUNBUFFERED=1 \
    PATH="/venv/bin:${PATH}"
COPY --from=builder /venv /venv
WORKDIR /app
COPY ./src .
RUN pip install ./wh_control
CMD python -m aiohttp.web -H localhost -P 8080 wired_up.api.main:init

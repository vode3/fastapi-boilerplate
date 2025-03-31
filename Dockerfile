FROM ghcr.io/astral-sh/uv:0.6-python3.13-bookworm-slim

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_FROZEN=1

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --no-install-project --no-editable --no-dev

ADD . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-editable --no-dev

ENV UV_NO_SYNC=1
ENV UV_NO_CACHE=1

CMD ["uv", "run", "--no-dev", "app"]

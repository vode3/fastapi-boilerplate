import logging
import multiprocessing as mp
from typing import Any

import uvicorn

from app.config import ServerConfig


class _HealthcheckFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return "/health/" not in record.getMessage()


def _get_workers_count() -> int:
    return mp.cpu_count() - 1


def run_uvicorn(app: Any, config: ServerConfig, workers: int | None = None, **kw: Any) -> None:
    uv_config = uvicorn.Config(
        app,
        host=config.host,
        port=config.port,
        log_level=config.log_level,
        reload=config.debug,
        workers=workers or _get_workers_count(),
        forwarded_allow_ips="*",
        loop="uvloop",
        **kw,
    )

    for name in logging.root.manager.loggerDict:
        if name.startswith("uvicorn."):
            logger = logging.getLogger(name)
            logger.addFilter(_HealthcheckFilter())

    server = uvicorn.Server(uv_config)
    server.run()

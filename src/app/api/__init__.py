from typing import Any

from fastapi import APIRouter
from fastapi import FastAPI

from app.api.common.exceptions import setup_exception_handlers
from app.api.common.responses import ORJSONResponse
from app.api.healthcheck import healthcheck_router
from app.config import Config


def setup_controllers(app: FastAPI) -> None:
    router = APIRouter(prefix="/api")

    app.include_router(router=healthcheck_router)
    app.include_router(router=router)


def init_app(config: Config, **kw: Any) -> FastAPI:
    app = FastAPI(
        default_response_class=ORJSONResponse,
        title=config.server.title,
        version=config.server.version,
        debug=config.server.debug,
        docs_url="/docs" if config.server.debug else None,
        redoc_url="/redoc" if config.server.debug else None,
        swagger_ui_oauth2_redirect_url=None,
        **kw,
    )

    setup_controllers(app)
    setup_exception_handlers(app)

    return app

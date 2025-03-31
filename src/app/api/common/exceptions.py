from collections.abc import Awaitable
from collections.abc import Callable
from functools import partial

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request

from app.api.common.responses import ORJSONResponse
from app.common.exceptions import AppException
from app.common.exceptions import BadRequestError
from app.common.exceptions import ConflictError
from app.common.exceptions import ForbiddenError
from app.common.exceptions import NotFoundError
from app.common.exceptions import ServiceNotImplementedError
from app.common.exceptions import ServiceUnavailableError
from app.common.exceptions import TooManyRequestsError
from app.common.exceptions import UnAuthorizedError


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(BadRequestError, error_handler(400))
    app.add_exception_handler(ConflictError, error_handler(409))
    app.add_exception_handler(ForbiddenError, error_handler(403))
    app.add_exception_handler(NotFoundError, error_handler(404))
    app.add_exception_handler(ServiceNotImplementedError, error_handler(501))
    app.add_exception_handler(ServiceUnavailableError, error_handler(503))
    app.add_exception_handler(TooManyRequestsError, error_handler(429))
    app.add_exception_handler(UnAuthorizedError, error_handler(401))
    app.add_exception_handler(AppException, app_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unknown_exception_handler)


async def unknown_exception_handler(request: Request, err: Exception) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "detail": "Unknown error",
            "additional": [],
        },
    )


async def validation_exception_handler(
    request: Request, err: RequestValidationError
) -> ORJSONResponse:
    return ORJSONResponse(
        {
            "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "detail": [
                {"field": err.get("loc")[-1], "detail": err.get("msg")} for err in err._errors
            ],
            "additional": [
                {"field": err.get("loc")[-1], "additional": err.get("ctx")} for err in err._errors
            ],
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


def error_handler(
    status_code: int,
) -> Callable[..., Awaitable[ORJSONResponse]]:
    return partial(app_error_handler, status_code=status_code)


async def app_error_handler(
    request: Request, err: AppException, status_code: int
) -> ORJSONResponse:
    return await handle_error(request=request, err=err, status_code=status_code)


async def handle_error(request: Request, err: AppException, status_code: int) -> ORJSONResponse:
    return ORJSONResponse(**err.as_dict(), status_code=status_code)

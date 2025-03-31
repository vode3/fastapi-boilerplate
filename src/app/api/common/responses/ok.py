from collections.abc import Mapping

from starlette.background import BackgroundTask
from starlette.status import HTTP_200_OK

from app.api.common.responses.orjson import ORJSONResponse


class OkResponse[R](ORJSONResponse):
    def __init__(
        self,
        content: R,
        status_code: int = HTTP_200_OK,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        super().__init__(content, status_code, headers, media_type, background)

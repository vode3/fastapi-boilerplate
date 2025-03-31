from typing import Any

from fastapi.responses import ORJSONResponse as _ORJSONResponse

from app.api.common.responses.serializers.orjson import orjson_dumps


class ORJSONResponse(_ORJSONResponse):
    def render(self, content: Any) -> bytes:
        if isinstance(content, str):
            return content.encode()
        if isinstance(content, bytes):
            return content
        return orjson_dumps(content)

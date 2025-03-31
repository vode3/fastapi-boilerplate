from pydantic import BaseModel
from pydantic import Field


class PaginationInfo(BaseModel):
    limit: int = 0
    next_cursor: str | None = None


class PaginationResponse[R: BaseModel](BaseModel):
    items: list[R] = Field(default_factory=list)
    pagination: PaginationInfo = Field(default_factory=PaginationInfo)

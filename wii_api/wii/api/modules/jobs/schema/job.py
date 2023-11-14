from pydantic import Field

from api.modules._shared.schema.base import WhereIsItPayload, WhereIsItResponseModel
from ..models import JobRequestStatusEnum


class JobRequestPost(WhereIsItPayload):
    title: str
    is_movie: bool = Field(
        default=False,
    )
    is_tv: bool = Field(
        default=False,
    )
    is_actor: bool = Field(
        default=False,
    )
    is_director: bool = Field(
        default=False,
    )


class JobRequestResponse(WhereIsItResponseModel):
    title: str
    is_movie: bool
    is_tv: bool
    is_actor: bool
    is_director: bool
    status: JobRequestStatusEnum
    redis_result: dict | None = None

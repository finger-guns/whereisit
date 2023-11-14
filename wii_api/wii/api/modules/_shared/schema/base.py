from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class _Config(BaseModel):
    model_config = ConfigDict(
        ser_json_timedelta="iso8601",
        use_enum_values=True,
    )


class WhereIsItBaseModel(_Config):
    pass


class WhereIsItPartialResponse(WhereIsItBaseModel):
    id: Any


class WhereIsItResponseModel(WhereIsItPartialResponse):
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
    deleted: bool = False


class WhereIsItPatchPayload(_Config):
    updated_at: datetime


class WhereIsItPayload(_Config):
    pass

class WhereIsItDelete(_Config):
    id: UUID

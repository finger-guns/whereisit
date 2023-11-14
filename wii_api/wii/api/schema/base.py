from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel, to_snake


class _Config(BaseModel):
    model_config = ConfigDict(
        ser_json_timedelta="iso8601",
        use_enum_values=True,
    )


class WhereIsItBaseModel(_Config):
    pass


class WhereIsItPartialResponse(WhereIsItBaseModel):
    id: UUID


class WhereIsItResponseModel(WhereIsItPartialResponse):
    model_config = ConfigDict(alias_generator=to_camel)

    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
    deleted: bool = False


class WhereIsItPatchPayload(_Config):
    updated_at: datetime


class WhereIsItPayload(_Config):
    model_config = ConfigDict(alias_generator=to_snake)


class WhereIsItDelete(_Config):
    id: UUID

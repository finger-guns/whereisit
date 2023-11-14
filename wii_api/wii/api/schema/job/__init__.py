from ..base import WhereIsItPayload

from pydantic import Field

class JobRequest(WhereIsItPayload):
    title: str
    movie: bool = Field(default=False)
    tv: bool = Field(default=False)

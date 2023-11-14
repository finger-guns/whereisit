from typing import Optional

from fastapi import HTTPException
from pydantic import Field

from .base import WhereIsItBaseModel

GENERAL_ERROR_MESSAGE: str = (
    "An error message that may contain techincal jargon and be messy"
)


class GeneralError(WhereIsItBaseModel):
    user_message: str = Field(
        "Invalid request to server",
        title="An error message to display for the user",
    )
    message: int = Field(
        None,
        title=GENERAL_ERROR_MESSAGE,
    )


class WhereIsItError(WhereIsItBaseModel):
    detail: GeneralError


class WhereIsItHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int,
        message: str,
        user_message: Optional[str] = "",
    ) -> None:
        if not message:
            raise ValueError("Invalid Wii Exception")

        self.detail = "Wii Exception"

        self.status_code = status_code
        self.message = message
        self.user_message = user_message

        if not user_message:
            self.user_message = message

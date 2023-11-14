from enum import Enum

from sqlalchemy import Boolean, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from api.modules._shared import DefaultMixin


class JobRequestStatusEnum(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class JobRequest(DefaultMixin):
    __tablename__ = "job_request"

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    is_movie: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    is_tv: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # NOT IMPLEMENTED YET.
    is_actor: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    is_director: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    status: Mapped[JobRequestStatusEnum] = mapped_column(
        ENUM(
            JobRequestStatusEnum,
            name="job_request_status_enum",
            create_type=False,
        ),
        default=JobRequestStatusEnum.PENDING,
        nullable=False,
    )

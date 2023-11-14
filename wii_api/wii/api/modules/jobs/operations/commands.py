from collections.abc import Sequence
from typing import Any
from uuid import UUID

from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.types import UUID as PG_UUID

from api.utils.error_wrapper import catch_sql_errors
from ..models import JobRequest, JobRequestStatusEnum


@catch_sql_errors
async def insert_job(
    session: AsyncSession,
    title: str,
    is_movie: bool = False,
    is_tv: bool = False,
    is_actor: bool = False,
    is_director: bool = False,
) -> PG_UUID[Any] | None:
    if not any([is_movie, is_tv, is_actor, is_director]):
        raise ValueError(
            "At least one of is_movie, is_tv, is_actor, is_director must be True"
        )

    if not title:
        raise ValueError("Title must be provided")

    stmt = (
        insert(JobRequest)
        .values(
            title=title,
            is_movie=is_movie,
            is_tv=is_tv,
            is_actor=is_actor,
            is_director=is_director,
        )
        .returning(JobRequest.id)
    )

    result = await session.execute(stmt)
    return result.scalar()


@catch_sql_errors
async def update_job_request_status(
    session: AsyncSession,
    job_id: UUID | PG_UUID[Any],
    status: JobRequestStatusEnum = JobRequestStatusEnum.PROCESSING,
) -> JobRequestStatusEnum | None:
    stmt = (
        update(JobRequest)
        .where(
            JobRequest.id == job_id,
        )
        .values(
            status=status
        )
        .returning(
            JobRequest.status,
        )
    )

    result = await session.execute(stmt)
    return result.scalar()

from collections.abc import Sequence
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.types import UUID as PG_UUID

from api.utils.error_wrapper import catch_sql_errors
from api.utils.logger import info
from ..models import JobRequest, JobRequestStatusEnum


@catch_sql_errors
async def get_job_request_by_id(
    session: AsyncSession,
    job_id: UUID,
) -> JobRequest | None:
    info(
        message=f"Getting job request by id: {job_id}",
        path="get_job_request_by_id",
    )
    stmt = select(JobRequest,).where(
        JobRequest.id == job_id,
    )
    result = await session.execute(stmt)
    return result.scalar()


@catch_sql_errors
async def get_job_requests_by_status(
    session: AsyncSession, status: JobRequestStatusEnum = JobRequestStatusEnum.FAILED
) -> Sequence[PG_UUID[Any]]:
    info(
        message=f"Getting jobs with status {status}",
        path="get_job_requests_by_status",
    )
    stmt = select(JobRequest.id,).where(
        JobRequest.status == status,
    )
    result = await session.execute(stmt)
    return result.scalars().all()

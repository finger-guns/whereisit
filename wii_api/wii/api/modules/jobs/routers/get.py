from base64 import b64decode
from json import loads
from uuid import UUID

from fastapi import Depends
from fastapi.routing import APIRouter
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_418_IM_A_TEAPOT

from api.modules._shared.schema.error import WhereIsItHTTPException
from api.modules.jobs.operations.queries import get_job_request_by_id
from api.modules.jobs.schema.job import JobRequestResponse
from api.services.redis import get
from api.utils import get_async_db, info, redis
from api.utils.error_wrapper import catch_general_exceptions_to_http

router = APIRouter(
    tags=["jobs"],
)


@router.get("/{job_id}")
@catch_general_exceptions_to_http
async def handle_get_job_request_by_id(
    job_id: UUID,
    session: AsyncSession = Depends(get_async_db),
    redis_client: Redis = Depends(redis),
) -> JobRequestResponse | None:
    job = await get_job_request_by_id(
        session=session,
        job_id=job_id,
    )

    if not job:
        info(
            message=f"Job not found in database - {job_id}",
            path="handle_get_job_request_by_id",
        )
        raise WhereIsItHTTPException(
            status_code=HTTP_418_IM_A_TEAPOT,
            message="Could Not find Job.",
            user_message="Could not find job.",
        )

    redis_result = await get(redis_client, job_id)

    if not redis_result:
        info(
            message=f"Job not found in redis - {job_id}",
            path="handle_get_job_request_by_id",
        )
        raise WhereIsItHTTPException(
            status_code=HTTP_418_IM_A_TEAPOT,
            message="Could Not find Job.",
            user_message="Could not find job.",
        )
    
    return JobRequestResponse(
        id=job.id,
        title=job.title,
        is_tv=job.is_tv,
        is_movie=job.is_movie,
        is_actor=job.is_actor,
        is_director=job.is_director,
        status=job.status,
        redis_result=loads(b64decode(redis_result).decode("utf-8")) or None
    )

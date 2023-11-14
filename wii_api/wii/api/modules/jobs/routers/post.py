import re
from json import dumps
from uuid import UUID

from fastapi import Depends
from fastapi.routing import APIRouter
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_418_IM_A_TEAPOT

from api.modules._shared.schema.error import WhereIsItHTTPException
from api.modules.jobs.schema.job import JobRequestPost, JobRequestResponse
from api.services.redis import publish
from api.utils import error, get_async_db, info, redis
from api.utils.error_wrapper import catch_general_exceptions_to_http
from ..models import JobRequestStatusEnum
from ..operations.commands import insert_job, update_job_request_status

router = APIRouter(
    tags=["jobs"],
)


@router.post("/")
@catch_general_exceptions_to_http
async def handle_insert_job(
    job_request: JobRequestPost,
    session: AsyncSession = Depends(get_async_db),
    redis_client: Redis = Depends(redis),
) -> JobRequestResponse | None:

    job_id = await insert_job(
        session=session,
        title=job_request.title,
        is_tv=job_request.is_tv,
        is_movie=job_request.is_movie,
        is_actor=job_request.is_actor,
        is_director=job_request.is_director,
    )
    await session.commit()

    if not job_id:
        error(
            message=f"Could not insert job - {dict(job_request)}",
            path="handle_new_job",
        )
        raise WhereIsItHTTPException(
            status_code=HTTP_418_IM_A_TEAPOT,
            message="Job ID Was NONE",
            user_message="Could not handle job request at the moment.",
        )

    status = await publish(
        redis=redis_client,
        channel="to-scrape",
        message=dumps(
            {
                **job_request.model_dump(),
                "job_id": str(job_id),
            }
        ),
    )

    result = await update_job_request_status(
        session=session,
        job_id=job_id,
        status=JobRequestStatusEnum.PROCESSING
        if status != 0
        else JobRequestStatusEnum.PENDING,
    )

    if not result:
        info(
            message=f"Could not update job status - {dict(job_request)}",
            path="handle_new_job",
        )

    return JobRequestResponse(
        id=job_id,
        title=job_request.title,
        is_movie=job_request.is_movie,
        is_tv=job_request.is_tv,
        is_actor=job_request.is_actor,
        is_director=job_request.is_director,
        status=result if result else JobRequestStatusEnum.PENDING,
    )

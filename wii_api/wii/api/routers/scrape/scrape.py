from uuid import UUID, uuid4
from base64 import b64decode
from json import dumps, loads

from api.utils.redis import redis
from api.utils.logger import info
from api.services.redis import get, publish
from api.schema.job import JobRequest
from api.utils.error_wrapper import catch_general_exceptions_to_http

from fastapi import APIRouter, Depends, HTTPException
from redis.asyncio import Redis


router = APIRouter(
    prefix="/scrape",
    tags=["scrape"],
)


@catch_general_exceptions_to_http
@router.post("/job")
async def scrape_job_request(
    job_request: JobRequest,
    redis_client: Redis = Depends(redis),
):
    """
    This is going to be the endpoint that the frontend hits to start a scrape job
    the body will be the exact same as the actual go side of things so something like this.
    {
    "movie": False,
    "tv": True,
    "title": "Ash Vs Evil"
    }
    It'll reply with a request id.
    """
    job_id = uuid4()

    info(f"job_request {job_id} received")

    request = dumps({
        **job_request.model_dump(),
        "job_id": str(job_id),
    })

    info(f"job_request {job_id} publishing")
    
    await publish(
        redis=redis_client,
        channel="to-scrape",
        message=request,
    )

    info(f"job_request {job_id} published")
    return {"message": job_id}


@router.get("/job/{job_id}")
async def scrape_job_status(
    job_id: UUID,
    redis_client: Redis = Depends(redis),
):
    """
    This is going to be the endpoint that the frontend hits to check the status of a scrape job
    """
    result = await get(redis_client, job_id)

    if not result:
        raise HTTPException(status_code=404, detail="Job not found")

    return loads(b64decode(result).decode('utf-8'))

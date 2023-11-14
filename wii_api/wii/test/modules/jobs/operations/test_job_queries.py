from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from api.modules.jobs.operations.commands import insert_job
from api.modules.jobs.operations.queries import get_job_request_by_id


async def test_get_job_request_by_id(
    session: AsyncSession,
) -> None:
    job_id = await insert_job(
        session=session,
        title="Test Title",
        is_tv=True,
        is_movie=False,
        is_actor=False,
        is_director=False,
    )
    assert job_id
    await session.commit()

    returned_job = await get_job_request_by_id(
        session=session, job_id=UUID(str(job_id))
    )
    assert returned_job is not None

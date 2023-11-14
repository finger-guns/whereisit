from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from api.modules.jobs.operations.commands import insert_job, update_job_request_status


async def test_insert_new_job(
    session: AsyncSession,
) -> None:
    job = await insert_job(
        session=session,
        title="Test Title",
        is_tv=True,
        is_movie=False,
        is_actor=False,
        is_director=False,
    )
    assert job

    stmt = text("select * from job_request where title ilike :title")
    result = await session.execute(stmt, {"title": "Test Title"})
    assert result is not None


async def test_patch_job_request_status(
    session: AsyncSession,
) -> None:
    job = await insert_job(
        session=session,
        title="Test Title",
        is_tv=True,
        is_movie=False,
        is_actor=False,
        is_director=False,
    )
    assert job

    job_id = job

    job = await update_job_request_status(
        session=session,
        job_id=job_id,
        status="COMPLETED",
    )
    assert job

    stmt = text("select * from job_request where id = :id")
    result = await session.execute(stmt, {"id": job_id})
    assert result is not None
    assert result.fetchone().status == "COMPLETED"

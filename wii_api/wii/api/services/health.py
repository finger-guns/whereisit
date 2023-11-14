from api.utils.error_wrapper import catch_sql_errors
from api.utils.logger import error, info
from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession


@catch_sql_errors
async def healthy_db(
    session: AsyncSession,
) -> dict[str, int | str | bool | None] | None:
    stmt = text("SELECT 1")
    res = (await session.execute(stmt)).scalar()
    if not res:
        error(message="Not connected to database.", path="healthy_db", exc_info=None)
        return {"connected": False}

    info(message="Connected to database", path="healthy_db", exc_info=None)
    return {
        "connected": True,
        "result": res,
    }

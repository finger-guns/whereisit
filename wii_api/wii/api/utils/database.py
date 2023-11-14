from typing import AsyncIterator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from api.config import EnvironmentTypes, get_settings
from api.utils.logger import error

# --------------------------------------------------------------------------------
settings = get_settings()
# --------------------------------------------------------------------------------


def get_url(engine: str, db_name: str = settings.DATABASE_NAME):
    """Generate the psycop2 sqlalchemy connection string based on local env settings"""

    SQLALCHEMY_DATABASE_URL = f"postgresql+{engine}://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{db_name}"

    if settings.ENVIRONMENT_TYPE != EnvironmentTypes.LOCAL:
        SQLALCHEMY_DATABASE_URL = (
            f"postgresql+{engine}://{settings.DATABASE_USER}:"
            f"{settings.DATABASE_PASSWORD}@/{db_name}"
            f"{settings.DATABASE_HOST}"
        )

    return SQLALCHEMY_DATABASE_URL


db_config = {
    # Pool size is the maximum number of permanent connections to keep.
    "pool_size": 5,
    # Temporarily exceeds the set pool_size if no connections are available.
    "max_overflow": 2,
    "pool_timeout": 30,  # 30 seconds
    # 'pool_recycle' is the maximum number of seconds a connection can persist.
    "pool_recycle": 1800,  # 30 minutes
}

async_engine = create_async_engine(
    get_url("asyncpg"),
    pool_pre_ping=True,
    echo=False,
    **db_config,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    expire_on_commit=False,
)



async def get_async_db() -> AsyncIterator[AsyncSession]:
    try:
        async with AsyncSessionLocal() as session:
            yield session
    except SQLAlchemyError as e:
        error(
            message="database error",
            path="get_async_db",
            exc_info=e,
        )

from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from .config import EnvironmentTypes, get_settings
from .modules.jobs import job_router
from .schema.error import WhereIsItHTTPException
from .services.health import healthy_db
from .utils.database import get_async_db
from .utils.logger import configure_logger

settings = get_settings()

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)

configure_logger()


if settings.ENVIRONMENT_TYPE != EnvironmentTypes.PRODUCTION:
    app.debug = True

origins = [
]


if settings.ENVIRONMENT_TYPE == EnvironmentTypes.LOCAL:
    origins.append("*")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.router.redirect_slashes = False

base_router = APIRouter(
    prefix="/api",
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_: Request, exc):
    """
    Override default exception handler to return better exceptions for frontend
    """
    if exc.detail == "Frowny Exception":
        error_detail = {
            "detail": {
                "user_message": exc.user_message,
                "message": exc.message,
            }
        }

    else:
        error_detail = {
            "detail": {
                "user_message": "Invalid request to server",
                "message": str(exc.detail),
            }
        }

    return JSONResponse(
        content=error_detail,
        status_code=exc.status_code,
    )


@app.get("/ping")
def handle_ping_pong() -> Dict[str, str]:
    return {"ping": "pong"}


@app.get("/healthz", response_model=int)
def handle_healthz() -> int:
    return HTTP_200_OK


@app.get("/readyz", response_model=int)
async def handle_readyz(session: AsyncSession = Depends(get_async_db)) -> int:
    response = await healthy_db(session=session)

    if not response:
        raise WhereIsItHTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            user_message="Database is not healthy",
            message="Database is not healthy",
        )

    if not response["connected"]:
        raise WhereIsItHTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            user_message="Database is not healthy",
            message="Database is not healthy",
        )

    return HTTP_200_OK


base_router.include_router(
    job_router,
)

app.include_router(base_router)

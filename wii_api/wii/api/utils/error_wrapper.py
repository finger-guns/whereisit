from asyncio import iscoroutinefunction
from functools import wraps
from traceback import format_exc

from fastapi import HTTPException, status
from sqlalchemy.exc import DatabaseError, SQLAlchemyError

from api.config import get_settings
from api.modules import WhereIsItHTTPException
from .logger import error

settings = get_settings()


def catch_general_exceptions_to_http(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            if iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        except Exception as e:
            print(e)
            error_message = format_exc()
            if not isinstance(e, (HTTPException, WhereIsItHTTPException)):
                user_msg = settings.BACKEND_ERROR_MESSAGE
                if settings.RETURN_EXCEPTION_REASON:
                    raise WhereIsItHTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        message=error_message,
                        user_message=user_msg,
                    )
                else:
                    raise WhereIsItHTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        message=user_msg,
                        user_message=user_msg,
                    )
            else:
                raise e

    return wrapper


def catch_sql_errors(func):
    """Decorator to catch SQLAlchemy errors"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            if iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        except (DatabaseError, SQLAlchemyError, Exception) as e:
            error(
                message="SQLAlchemy database error occurred",
                path=func.__name__,
                exc_info=e,
            )
            return None

    return wrapper


def catch_general_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_message = format_exc()
            if isinstance(e, SQLAlchemyError):
                user_msg = settings.BACKEND_ERROR_MESSAGE
                if settings.RETURN_EXCEPTION_REASON:
                    raise WhereIsItHTTPException(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        message=error_message,
                        user_message=user_msg,
                    )
                else:
                    raise WhereIsItHTTPException(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        message=user_msg,
                        user_message=user_msg,
                    )
            elif not isinstance(e, (HTTPException, WhereIsItHTTPException)):
                user_msg = settings.BACKEND_ERROR_MESSAGE
                if settings.RETURN_EXCEPTION_REASON:
                    raise WhereIsItHTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        message=error_message,
                        user_message=user_msg,
                    )
                else:
                    raise WhereIsItHTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        message=user_msg,
                        user_message=user_msg,
                    )
            else:
                raise e

    return wrapper

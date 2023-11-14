from logging import Logger, config, getLogger

from api.config import WhereIsItLogConfig


def configure_logger():
    config.dictConfig(WhereIsItLogConfig().model_dump())


def logger() -> Logger:
    return getLogger(WhereIsItLogConfig().LOGGER_NAME)


def info(
    message: str = "Something interesting happened",
    path: str = "UNKNOWN",
    exc_info: Exception | None = None,
):
    logger().info(message, extra={"path": path}, exc_info=exc_info)


def debug(
    message: str = "Something interesting happened",
    path: str = "UNKNOWN",
    exc_info: Exception | None = None,
):
    print(f""" {path} - \n\n {message} - \n\n """)
    logger().debug(message, extra={"path": path}, exc_info=exc_info)


def warning(
    message: str = "Something interesting happened",
    path: str = "UNKNOWN",
    exc_info: Exception | None = None,
):
    logger().warning(message, extra={"path": path}, exc_info=exc_info)


def error(
    message: str = "Something interesting happened",
    path: str = "UNKNOWN",
    exc_info: Exception | None = None,
):
    logger().error(message, extra={"path": path}, exc_info=exc_info)

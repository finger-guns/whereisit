from dataclasses import dataclass
from os import getenv
from logging import basicConfig, DEBUG


@dataclass
class Config:
    REDIS_HOST: str = getenv('REDIS_HOST', default='localhost')
    REDIS_PORT: int = int(getenv('REDIS_PORT', default='6379'))

    POSTGRES_HOST: str = getenv('POSTGRES_HOST', default='localhost')
    POSTGRES_PORT: str = getenv('POSTGRES_PORT', default='5432')
    POSTGRES_USER: str = getenv('POSTGRES_USER', default='postgres')
    POSTGRES_PASSWORD: str = getenv('POSTGRES_PASSWORD', default='postgres')
    POSTGRES_DATABASE: str = getenv('POSTGRES_DB', default='postgres')


def init_logging(
    log_level=DEBUG,
    log_file=None,
) -> None:
    """Set up basic logging configuration."""
    if log_file:
        basicConfig(filename=log_file, level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')


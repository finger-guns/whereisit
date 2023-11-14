FROM python:3.12-slim

WORKDIR /app

ENV POETRY_VERSION=1.6.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

RUN pip install "poetry==$POETRY_VERSION"

COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry install --no-dev

RUN poetry add hupper

COPY ./src /app/src

CMD ["python", "/app/src/main.py"]

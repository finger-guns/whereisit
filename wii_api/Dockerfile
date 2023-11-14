# Base image
FROM python:3.12.0-slim-bullseye AS base

ENV PORT=8000
EXPOSE ${PORT}

# Set working directory
WORKDIR /app

COPY ./wii/poetry.lock ./wii/pyproject.toml /app/

# Install dependencies
RUN apt-get update \
    && apt-get install libpq-dev gcc -y \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install poetry

# Copy project files
COPY ./wii/api /app/api

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-dev

# Provide default arguments, including the PORT environment variable
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

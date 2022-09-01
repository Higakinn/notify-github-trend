FROM python:3.8-slim

RUN apt-get update && apt-get install -y curl

RUN pip install poetry

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN poetry install

COPY . .

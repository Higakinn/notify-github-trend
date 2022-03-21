FROM python:3.8-slim

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH /root/.poetry/bin:$PATH

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN poetry install

COPY . .
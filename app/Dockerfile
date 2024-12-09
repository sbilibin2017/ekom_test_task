FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

COPY ../pyproject.toml /pyproject.toml

RUN poetry install --only main

COPY . .

EXPOSE ${APP_PORT}
FROM python:3.12.9-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV IS_DOCKER 1

RUN apt-get -y update && apt-get -y install curl

WORKDIR /service

COPY README.md .
COPY pyproject.toml .
COPY alembic.ini .

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

COPY src src
COPY migrations migrations

EXPOSE 8080

CMD bash -c "cd src && poe migrate && poe start"
FROM python:3.8-slim-buster as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/scripts:${PATH}"

ARG DEBIAN_FRONTEND=noninteractive

# General installs
RUN apt-get update && apt-get --no-install-recommends install -y \
    git \
    curl \
    python3-dev \
    build-essential

# Build requirements wheels
WORKDIR /tmp
RUN pip install --upgrade pip

RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

#COPY requirements.txt requirements.txt


RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt


FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ARG DEBIAN_FRONTEND=noninteractive

EXPOSE 8000

# General installs
RUN apt-get update && apt-get --no-install-recommends install -y git curl

# Purge build dependencies
RUN rm -rf /var/lib/apt/lists/* && apt-get clean


RUN addgroup --system django && \
    adduser --system --ingroup django --home /app django
USER django

WORKDIR /app
ENV PATH=${PATH}:/app/.local/bin

# install requirements
COPY --from=base /wheels /wheels
COPY --from=base /tmp/requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

COPY --chown=django:django . /app

CMD ["gunicorn", "works.wsgi", "--bind", "0.0.0.0:8000", "--log-level", "debug", "--timeout", "30", "--worker-connections", "1000", "--workers", "3", "--threads", "2", "--access-logfile", "-", "--chdir", "/app"]

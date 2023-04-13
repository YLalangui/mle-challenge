FROM python:3.9-slim

ENV HOMEDIR=/app

RUN apt-get update --fix-missing
RUN apt-get install -y git make

RUN mkdir -p $HOMEDIR
COPY . $HOMEDIR
WORKDIR $HOMEDIR
ENV PYTHONPATH='$PYTHONPATH:/app'

RUN pip install --no-cache-dir --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-dev

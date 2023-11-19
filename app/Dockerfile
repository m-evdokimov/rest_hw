FROM python:3.10-slim

WORKDIR /app
COPY . /app/

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

EXPOSE 8000

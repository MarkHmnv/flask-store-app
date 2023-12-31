FROM python:3.11-alpine
LABEL maintainer="MarkHmnv"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        flask-user && \
    mkdir /instance && \
    chown flask-user:flask-user /instance

ENV PATH="/py/bin:$PATH"

USER flask-user
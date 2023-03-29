FROM python:3.11

RUN adduser app

COPY --chown=app:app ./src /opt

USER app
WORKDIR /opt

RUN --mount=type=cache,target=/home/app/.cache \
    pip3 install --upgrade --user -r requirements.txt

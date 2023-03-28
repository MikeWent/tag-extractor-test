FROM python:3.11

RUN adduser app

COPY project            /opt/project
COPY alembic            /opt/alembic

COPY alembic.ini        /opt/
COPY uvicorn-log.yml    /opt/
COPY requirements.txt   /opt/

USER app
WORKDIR /opt

RUN --mount=type=cache,target=/home/app/.cache \
    pip3 install --upgrade --user -r requirements.txt

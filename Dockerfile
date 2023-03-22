FROM python:3.11

COPY tagextractor           /opt/tagextractor
COPY requirements.txt       /opt/
COPY uvicorn-logging.yml    /opt/

WORKDIR /opt
RUN --mount=type=cache,target=/root/.cache \
    pip3 install --upgrade -r requirements.txt

CMD ["uvicorn", "tagextractor.app:app", "--log-config", "uvicorn-logging.yml", "--host", "0.0.0.0", "--port", "8080"]

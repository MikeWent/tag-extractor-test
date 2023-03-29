from os import getenv

from celery import Celery

celery_app = Celery("worker", broker=getenv("CELEREY_BROKER_URL"))

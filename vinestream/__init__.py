# to make sure celery is loaded when django starts
from .celery import app as celery_app
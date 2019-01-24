from django.conf import settings
import os
from celery import Celery

# set default configuration for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vinestream.settings')

# create our app instance
app = Celery('vinestream')

# set custom configuration for celery
app.config_from_object('django.conf:settings')

# set celery to autodiscover asynchronous tasks
app.autodiscover_tasks(lambda : settings.INSTALLED_APPS)


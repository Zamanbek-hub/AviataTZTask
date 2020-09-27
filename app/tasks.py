# Create your tasks here
from celery import shared_task
from celery.schedules import crontab
from datetime import datetime

from .services import do_requests_and_feel_cache

# @periodic_task(run_every=crontab(minutes='*/6'), name="my_first_task")
def my_first_task():
    print("First function launched {}".format(datetime.now()))

@shared_task
def my_second_task():
     print("Second function launched {}".format(datetime.now()))


@shared_task
def my_third_task():
     print("Third function launched {}".format(datetime.now()))


# @shared_task
# def feel_cache_about_lines():
#     do_requests_and_feel_cache()

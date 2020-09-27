# Create your tasks here

from celery import shared_task
# from celery.task import periodic_task
from celery.schedules import crontab
from datetime import datetime

# @periodic_task(run_every=crontab(minutes='*/6'), name="my_first_task")
def my_first_task():
    print("First function launched {}".format(datetime.now()))

@shared_task
def my_second_task():
     print("Second function launched {}".format(datetime.now()))


@shared_task
def my_third_task():
     print("Third function launched {}".format(datetime.now()))

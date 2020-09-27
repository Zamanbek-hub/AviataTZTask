# Create your tasks here
from celery import shared_task
from celery.schedules import crontab
from datetime import datetime

from .services import do_requests_and_feel_cache, do_requests_to_check_finded_cheap_tickets


@shared_task
def feel_cache_about_lines():
    do_requests_and_feel_cache()
    print("done")


@shared_task
def check_flight():
    do_requests_to_check_finded_cheap_tickets()
    print("done")

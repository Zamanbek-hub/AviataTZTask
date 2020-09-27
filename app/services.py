from django.core.cache import cache
from .constants import URL
from django.utils import timezone
import datetime
import requests
from .models import *

import json


def json_response(something):
    return HttpResponse(
        json.dumps(something),
        content_type='application/javascript; charset=utf8'
    )


def _filter_data(data: dict) -> list():
    lines = []

    for d in data:
        line = {}
        line['flyFrom'] = d['flyFrom']
        line['cityFrom'] = d['cityFrom']
        line['flyTo'] = d['flyTo']
        line['cityTo'] = d['cityTo']
        line['distance'] = d['distance']
        line['fly_duration'] = d['fly_duration']
        line['price'] = d['price']
        line['booking_token'] = d['booking_token']
        lines.append(line)

    lines = sorted(lines, key=lambda k: k['price'])
    return lines


def do_requests_and_feel_cache():
    directions = Directions.objects.all()

    current_time = datetime.datetime.now().strftime("%d/%m/%Y")
    month_ahead = (datetime.datetime.now() +
                   datetime.timedelta(30)).strftime("%d/%m/%Y")

    for direct in directions:
        headers = {'Content-Type': 'application/json'}
        url = URL.format(
            direct.fly_from.code, direct.fly_to.code, current_time, month_ahead)

        response = requests.get(url, headers=headers)

        lineKey = "{0}:{1}".format(direct.fly_from.code,
                                   direct.fly_to.code)
        cheapLineKey = "{0}:{1}-cheapPrice".format(direct.fly_from.code,
                                                   direct.fly_to.code)

        filtered_data = _filter_data(response.json()['data'])
        cache.set(lineKey, filtered_data, 60 * 60)
        cache.set(cheapLineKey, filtered_data[0], 60 * 60)

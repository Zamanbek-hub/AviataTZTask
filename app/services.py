from django.core.cache import cache
from .constants import MAIN_URL, CHECK_FLIGHT_URL
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
    """ 
        return Filter taked JSON from MAIN_URL
    """

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

        print(line)
    lines = sorted(lines, key=lambda k: k['price'])
    return lines


def _do_api_requests(url:str):
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    return response

def _handle_main_url_request(direct:Directions):
    """ 
        To get url response and put them in Cache    
    """

    url = MAIN_URL.format(
            direct.fly_from.code, direct.fly_to.code, current_time, month_ahead)
        
    lineKey = "{0}:{1}".format(direct.fly_from.code,
                                direct.fly_to.code)
    cheapLineKey = "{0}:{1}-cheapPrice".format(direct.fly_from.code,
                                                direct.fly_to.code)

    filtered_data = _filter_data(_do_api_requests(url).json()['data'])
    cache.set(lineKey, filtered_data, 60 * 60)
    cache.set(cheapLineKey, filtered_data[0], 60 * 60)


def do_requests_and_feel_cache():
    """ 
        do request by all Directions to month ahead     
    """

    directions = Directions.objects.all()

    current_time = datetime.datetime.now().strftime("%d/%m/%Y")
    month_ahead = (datetime.datetime.now() +
                   datetime.timedelta(30)).strftime("%d/%m/%Y")

    for direct in directions:
        _handle_main_url_request(direct)
        


def do_requests_to_check_finded_cheap_tickets():
    """ 
        check to price_change to cheap line(ticket) by all Directions 
        in case price_change == True, overWrite new data to Cache
    """

    directions = Directions.objects.all()

    for direct in directions:
        cheapLineKey = "{0}:{1}-cheapPrice".format(direct.fly_from.code,
                                                   direct.fly_to.code)
        check_flight = cache.get(cheapLineKey)

        if check_flight:
            url = CHECK_FLIGHT_URL.format(check_flight['booking_token'])

            price_change = _do_api_requests(url).json()['price_change']
        
            if price_change:
                print("price_change True for: ",cheapLineKey)
                _handle_main_url_request(direct)
            else:
                print("price_change False for: ",cheapLineKey)
                


            


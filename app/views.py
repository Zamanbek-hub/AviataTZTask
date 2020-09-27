from django.shortcuts import render
from .models import *
from .serializers import CitySerializer
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from celery.schedules import crontab
from celery import shared_task
from .services import *
from .constants import *

# from celery.task import periodic_task
# Create your views here.


def home(request):
    return render(request, 'app/home.html')


@api_view(['GET'])
def fly_from_list(request):
    cities = City.objects.all().order_by('id')
    serializer = CitySerializer(cities, many=True)
    # cache.set('response', serializer.data, 60 * 60)
    return Response(serializer.data)


@api_view(['GET'])
def fly_to_list(request, id):
    directions = Directions.objects.filter(
        fly_from=City.objects.get(id=id))

    cities = []
    for direct in directions:
        cities.append(direct.fly_to)

    serializer = CitySerializer(cities, many=True)
    return Response(serializer.data)


def test(request):
    if request.method == "GET":
        time = datetime.datetime.now()
        formatedDate = time.strftime("%Y/%m/%d")
        print("datetime = ", time)
        print("datetime = ", type(formatedDate))
        print("datetime = ", time + datetime.timedelta(30))
    return render(request, 'app/home.html')


def testCron():
    print("Its Cdron")


@api_view(['GET'])
def get_cheap_line(request, flyFrom, flyTo):
    direct = Directions.objects.filter(
        fly_from=City.objects.get(id=flyFrom)).filter(
            fly_to=City.objects.get(id=flyTo)).get()

    fly_from = request.GET.get('flyFrom', None)
    fly_to = request.GET.get('flyTo', None)
    key = "{0}:{1}-cheapPrice".format(direct.fly_from.code,
                                      direct.fly_to.code)
    line = cache.get(key)

    if line:
        return Response(line)

    return Response(data={"Status:error"},  status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_lines(request, flyFrom, flyTo):

    direct = Directions.objects.filter(
        fly_from=City.objects.get(id=flyFrom)).filter(
            fly_to=City.objects.get(id=flyTo)).get()

    fly_from = request.GET.get('flyFrom', None)
    fly_to = request.GET.get('flyTo', None)
    key = "{0}:{1}".format(direct.fly_from.code,
                           direct.fly_to.code)
    lines = cache.get(key)

    if lines:
        return Response(lines)

    return Response(data={"Status:error"},  status=status.HTTP_404_NOT_FOUND)


def feel_cache(request):
    do_requests_and_feel_cache()
    return HttpResponse("Success")

    # class MyCronJob(CronJobBase):
    #     RUN_EVERY_SECONDS = 1  # every 2 hours

    #     schedule = Schedule(run_every_mins=RUN_EVERY_SECONDS)
    #     code = 'my_app.my_cron_job'    # a unique code

    #     def do(self):
    #         _testCron()    # do your thing here

from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.cache import cache

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


from .models import City, Directions
from .serializers import CitySerializer
from .services import do_requests_and_feel_cache, do_requests_to_check_finded_cheap_tickets
from .constants import MAIN_URL, CHECK_FLIGHT_URL



def home(request):
    return render(request, 'app/home.html')


@api_view(['GET'])
def fly_from_list(request):
    """
        Get all city objects
    """
    cities = City.objects.all().order_by('id')
    serializer = CitySerializer(cities, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def fly_to_list(request, id):
    """
        Get Direction fly_to City objects by fly_from(id)
    """
    exist = Directions.objects.filter(fly_from=City.objects.get(id=id)).exists()

    if exist:
        directions = Directions.objects.filter(fly_from=City.objects.get(id=id))

        cities = []
        for direct in directions:
            cities.append(direct.fly_to)

        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)
    
    return Response(data={"Status:error"},  status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def get_cheap_line(request, flyFrom, flyTo):
    """
        Get the cheapest line from particular Direction
    """

    exist = Directions.objects.filter(
                            fly_from=City.objects.get(id=flyFrom)).filter(
                                        fly_to=City.objects.get(id=flyTo)).get()

    if exist:
        direct = Directions.objects.filter(
                            fly_from=City.objects.get(id=flyFrom)).filter(
                                        fly_to=City.objects.get(id=flyTo)).get()

        fly_from = request.GET.get('flyFrom', None)
        fly_to = request.GET.get('flyTo', None)
        key = "{0}:{1}-cheapPrice".format(direct.fly_from.code,
                                        direct.fly_to.code)
        line = cache.get(key)

        if line is not None:
            return Response(line)

    return Response(data={"Status:error"},  status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_lines(request, flyFrom, flyTo):
    """
        Get all lines from particular Direction
    """

    exist = Directions.objects.filter(
                        fly_from=City.objects.get(id=flyFrom)).filter(
                                    fly_to=City.objects.get(id=flyTo)).exists()
 
    if exist:
        direct = Directions.objects.filter(
                            fly_from=City.objects.get(id=flyFrom)).filter(
                                        fly_to=City.objects.get(id=flyTo)).get()

        fly_from = request.GET.get('flyFrom', None)
        fly_to = request.GET.get('flyTo', None)

        if fly_from and fly_to:
            key = "{0}:{1}".format(direct.fly_from.code,
                                direct.fly_to.code)
            lines = cache.get(key)

            if lines is not None:
                return Response(lines)

    return Response(data={"Status:error"},  status=status.HTTP_404_NOT_FOUND)


def clear(request):
    cache.clear()
    return HttpResponse("Success")  
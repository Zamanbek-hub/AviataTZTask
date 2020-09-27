from django.urls import path
from .views import *

urlpatterns = [
     path('', home, name='home'),
     path('clear', clear, name='clear'),


     # DRF urls
     path('fly_from_list', fly_from_list, name='fly_from_list'),
     path('fly_to_list/<str:id>', fly_to_list, name='fly_to_list'),
     path('get_cheap_line/<flyFrom>/<flyTo>', get_cheap_line, name='get_cheap_line'),
     path('get_lines/<flyFrom>/<flyTo>', get_lines, name='get_lines'),
]

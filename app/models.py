from django.db import models

# Create your models here.


class City(models.Model):
    city = models.CharField('City name', max_length=255)
    code = models.CharField('City code', max_length=4)

    def __str__(self):
        return self.city + " : " + self.code


class Directions(models.Model):
    fly_from = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name='fly_from')
    fly_to = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name='fly_to')

    def __str__(self):
        return self.fly_from.code + " : " + self.fly_to.code

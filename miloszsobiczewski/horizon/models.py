from django.db import models
from django.contrib.auth.models import User


class Property(models.Model):

    location = models.CharField(max_length=100)
    size = models.IntegerField()
    type = models.CharField(max_length=100)
    unit_price = models.FloatField()
    total_price = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    link = models.CharField(max_length=500)
    date = models.DateField(auto_now=True, blank=True)
    like = models.BooleanField(default=False)

    def __str__(self):
        return self.location.__str__() #+ self.date.__str__()


class Filter(models.Model):

    property = models.CharField(max_length=100)
    max_price = models.IntegerField()
    min_price = models.IntegerField()
    max_size = models.IntegerField()
    min_size = models.IntegerField()

    def __str__(self):
        return self.property.__str__()

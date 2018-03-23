from django.db import models

# Create your models here. a blue print for your database

class Book(models.Model):
    name = models.CharField(max_length=100)
    count = models.IntegerField()

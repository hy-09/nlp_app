from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=50)
    url = models.CharField(max_length=200)
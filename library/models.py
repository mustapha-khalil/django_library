from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_year = models.DateTimeField("publication year")
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.title

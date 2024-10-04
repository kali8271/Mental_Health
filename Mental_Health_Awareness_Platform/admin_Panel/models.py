# admin/models.py

from django.db import models

class Professional(models.Model):
    name = models.CharField(max_length=100)
    expertise = models.CharField(max_length=100)

    def __str__(self):
        return self.name

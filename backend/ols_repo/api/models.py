from django.db import models
from random import randint
# Create your models here.


class Synonym (models.Model):
    label = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return f'{self.label}'


class Term (models.Model):
    label = models.TextField()
    description = models.TextField()
    id = models.CharField(
        max_length=32, default=f'FAKE_{randint(0, 9999999)}', primary_key=True)
    synonyms = models.ManyToManyField(Synonym)
    parents = models.ManyToManyField("self")
    def __str__(self):
        return self.label

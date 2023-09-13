from django.db import models
from random import randint
# Create your models here.


class Term (models.Model):
    label = models.CharField(max_length=256)
    description = models.TextField()
    id = models.CharField(
        max_length=12, default=f'FAKE_{randint(0, 9999999)}', primary_key=True)

    def __str__(self):
        return self.label


class Synonym (models.Model):
    label = models.CharField(max_length=256, unique=True)
    term_id = models.ForeignKey(Term, on_delete=models.CASCADE)

    def __str__(self):
        return self.label


class Ontology (models.Model):
    child_term_id = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="child_term")
    parent_term_id = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="parent_term")

    def __str__(self):
        return f'{self.parent_term_id} > {self.child_term_id}'

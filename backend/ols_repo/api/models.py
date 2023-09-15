from django.db import models
from random import randint
# Create your models here.


class Term (models.Model):
    label = models.TextField()
    description = models.TextField()
    id = models.CharField(
        max_length=32, default=f'FAKE_{randint(0, 9999999)}', primary_key=True)

    def __str__(self):
        return self.label


class Synonym (models.Model):
    label = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return f'{self.label}'


class SynonymAndTerm(models.Model):
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    synonym = models.ForeignKey(Synonym, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.synonym.label} === {self.term.label}'


class Ontology (models.Model):
    child_term = models.ForeignKey(
        Term, on_delete=models.CASCADE, related_name="child_term")
    parent_term = models.ForeignKey(
        Term, on_delete=models.CASCADE, related_name="parent_term")

    def __str__(self):
        return f'{self.parent_term} > {self.child_term}'

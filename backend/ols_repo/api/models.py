from django.db import models

# Create your models here.

class Term (models.Model):
    label = models.CharField(max_length=256)
    description = models.TextField()
    
    def __str__(self):
        return self.label
from django.contrib import admin

# Register your models here.

from .models import Term, Synonym, Ontology

admin.site.register(Term)
admin.site.register(Synonym)
admin.site.register(Ontology)
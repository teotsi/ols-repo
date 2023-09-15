from django.contrib import admin

# Register your models here.

from .models import Term, Synonym

admin.site.register(Term)
admin.site.register(Synonym)
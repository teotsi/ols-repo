from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from .models import Term
# Create your views here.


def home(request):
    return HttpResponse('done')


def terms(request):
    if request.method == "GET":
        all_terms = Term.objects.values()
        return JsonResponse({"terms": list(all_terms)})
    return HttpResponse('done')


def term(request):
    return HttpResponse('done')

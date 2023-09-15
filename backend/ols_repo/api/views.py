import json
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from .models import Term, Synonym
from .helpers import handle_server_errors, serialize_term, create_and_store_relationship

# Create your views here.


def home(request):
    return HttpResponse('done')


@csrf_protect
@csrf_exempt
@handle_server_errors
def terms(request):
    if request.method == "GET":
        all_terms = Term.objects.all()
        paginator = Paginator(all_terms, 20)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number or 0)
        print(paginator.num_pages)
        return JsonResponse({"terms": [serialize_term(term) for term in page_obj]})

    elif request.method == "POST":
        data = json.loads(request.body)
        # creating a new term
        new_term = Term.objects.create(
            id=data["id"], label=data["label"], description=data["description"])
        # storing term synonyms
        create_and_store_relationship(
            new_term, "synonyms", data, Synonym, "label")
        # storing parent rels
        create_and_store_relationship(new_term, "parents", data, Term, "id", defaults={
                                      "label": "unknown", "description": "unset"})
        return JsonResponse({"new_term": serialize_term(new_term)})

    return HttpResponse('Method not allowed', status=405)


@csrf_protect
@csrf_exempt
@handle_server_errors
def term(request, id):
    if request.method == "GET":

        term = Term.objects.get(id=id)
        return JsonResponse({"term": serialize_term(term)})

    elif request.method == "PUT":
        data = json.loads(request.body)
        Term.objects.filter(id=id).update(
            label=data["label"], description=data["description"])
        updated_term = Term.objects.get(id=id)
        return JsonResponse({"updated_term": model_to_dict(updated_term)})

    elif request.method == "DELETE":
        Term.objects.filter(id=id).delete()
        return JsonResponse({"deleted": True})

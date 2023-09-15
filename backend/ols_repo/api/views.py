import json
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from .models import Term, Synonym
from .helpers import handle_server_errors, serialize_term, create_and_store_relationship

# Create your views here.


@csrf_protect
@csrf_exempt
@handle_server_errors
def terms(request):
    """
    View handler for /terms.
    """
    if request.method == "GET":
        # retrieving all terms
        all_terms = Term.objects.all()
        # creating pagination
        paginator = Paginator(all_terms, 20)
        page_number = int(request.GET.get("page") or 1)
        page_obj = paginator.get_page(page_number)
        total_pages = paginator.num_pages

        return JsonResponse({
            "terms": [serialize_term(term) for term in page_obj],
            "pagination": {
                "current": page_number if page_number <= total_pages else total_pages,
                "pages": paginator.num_pages,
                "size": 20,
                "total": len(all_terms)
            }})

    elif request.method == "POST":
        data = json.loads(request.body)
        # creating a new term
        new_term = Term.objects.create(
            id=data["id"], label=data["label"], description=data["description"])
        # storing term synonyms
        create_and_store_relationship(
            new_term, "synonyms", data, Synonym, "label")
        # storing term parents
        create_and_store_relationship(new_term, "parents", data, Term, "id", defaults={
                                      "label": "unknown", "description": "unset"})

        return JsonResponse({"new_term": serialize_term(new_term)})

    return HttpResponse('Method not allowed', status=405)


@csrf_protect
@csrf_exempt
@handle_server_errors
def term(request, id):
    """
    View handler for /terms/<id>.
    """
    if request.method == "GET":

        term = Term.objects.get(id=id)
        return JsonResponse({"term": serialize_term(term)})

    elif request.method == "PUT":
        data = json.loads(request.body)
        Term.objects.filter(id=id).update(
            label=data["label"], description=data["description"])

        updated_term = Term.objects.get(id=id)
        # storing term synonyms
        create_and_store_relationship(
            updated_term, "synonyms", data, Synonym, "label")
        # storing term parents
        create_and_store_relationship(updated_term, "parents", data, Term, "id", defaults={
                                      "label": "unknown", "description": "unset"})
        return JsonResponse({"updated_term": serialize_term(updated_term)})

    elif request.method == "DELETE":
        Term.objects.filter(id=id).delete()
        return JsonResponse({"deleted": True})

    return HttpResponse('Method not allowed', status=405)

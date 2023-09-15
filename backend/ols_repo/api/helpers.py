from django.http import JsonResponse
from django.forms.models import model_to_dict


def handle_server_errors(fun):
    """
    decorator to handle missing resources and other server errors
    taken by any function.
    """
    def handler(*args, **kwargs):

        # storing time before function execution
        try:
            return fun(*args, **kwargs)
        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)}, status=400)
    return handler


def serialize_term(term):
    """
    simple helper to serialize nested fields in Term models
    :param term: The Term model to serialize
    """
    base_term = model_to_dict(term)
    base_term["synonyms"] = [str(synonym) for synonym in base_term["synonyms"]]
    base_term["parents"] = [parent.id for parent in base_term["parents"]]
    return base_term


def create_and_store_relationship(term, property, data, model, key, defaults={}):
    """
    Helper that helps with optional properties that may or may not exist already in the DB
    If the incoming request contains the property passed, then we iterate over it and for each
    item we add it to the many-to-many field of the selected Model. If the item does not exist,
    we create it before adding.
    """
    if property in data:
        for item in data[property]:
            query_args = {key: item, "defaults": defaults}
            query_result = model.objects.get_or_create(**query_args)
            # this translates to term.synonyms or term.parents,
            # but we need to get that via a string
            getattr(term, property).add(query_result[0])

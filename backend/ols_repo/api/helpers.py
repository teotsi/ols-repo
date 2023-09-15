from django.http import JsonResponse
from django.forms.models import model_to_dict

# decorator to handle missing resources and other server errors
# taken by any function.


def handle_server_errors(fun):
    def handler(*args, **kwargs):

        # storing time before function execution
        try:
            return fun(*args, **kwargs)
        except Exception as e:
            print(e)
            return JsonResponse({"error": str(e)}, status=400)
    return handler


def serialize_term(term):
    base_term = model_to_dict(term)
    base_term["synonyms"] = [str(synonym) for synonym in base_term["synonyms"]]
    base_term["parents"] = [parent.id for parent in base_term["parents"]]
    return base_term


def create_and_store_relationship(term, property, data, model, key, defaults={}):
    if property in data:
        for item in data[property]:
            print(item)
            query_args = {key: item, "defaults": defaults}
            print(query_args)
            query_result = model.objects.get_or_create(**query_args)
            try:
                print(query_result[0].id)
                print(query_result[0].parents)
            except:
                pass
            getattr(term, property).add(query_result[0])
            try:
                query_result[0].refresh_from_db()
                print(query_result[0].id)
                print(query_result[0].parents)
            except Exception as e:
                print(e)
                pass

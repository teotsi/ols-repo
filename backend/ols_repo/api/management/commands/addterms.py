from django.core.management.base import BaseCommand, CommandError
import requests
from api.models import Term, Synonym, SynonymAndTerm, Ontology
import aiohttp
import asyncio
from aiohttp.client_exceptions import ServerDisconnectedError
from tqdm.asyncio import tqdm


async def get_term_parents(session, url):
    fetched = False
    while not fetched:
        try:
            async with session.get(url) as resp:
                fetched = True
                page = await resp.json()
                return page
        except ServerDisconnectedError:
            await asyncio.sleep(10)


async def get_page(session, page_index):
    async with session.get(f"https://www.ebi.ac.uk/ols/api/ontologies/efo/terms?page={page_index}&size=500") as resp:
        page = await resp.json()
        return page


async def create_term_task(term):
    new_term = await Term.objects.acreate(  # creating and saving the new term
        label=term["label"], description="".join(term["description"]), id=term["short_form"])
    for synonym in term["synonyms"]:
        try:
            new_synonym = await Synonym.objects.acreate(  # creating and saving each synonym
                label=synonym)
            new_synonym_term_relationship = await SynonymAndTerm.objects.acreate(synonym=new_synonym, term=new_term)
        except Exception as e:
            print(e)
    return new_term


async def create_ontology_task(term, parents, mapping):
    if parents:
        for parent in parents["_embedded"]["terms"]:
            try:
                new_ontology_relationship = await Ontology.objects.acreate(
                child_term=term, parent_term=mapping[parent["short_form"]])
            except:
                pass

async def get_none():
    return None


class Command(BaseCommand):
    help = "Fetches terms from OLS and populates the DB"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("term_limit", nargs="?", type=int)

    def handle(self, *args, **options):
        upper_limit = options["term_limit"]
        Term.objects.all().delete()
        Synonym.objects.all().delete()

        initial_data_request = requests.get(
            "https://www.ebi.ac.uk/ols/api/ontologies/efo/terms")
        initial_data = initial_data_request.json()

        pagination_data = initial_data["page"]
        total_items = upper_limit or pagination_data["totalElements"]
        total_pages = total_items // 500 + 1
        last_page_remainder = total_items % 500
        if last_page_remainder == 0:
            total_pages -= 1

        async def main():
            async with aiohttp.ClientSession() as session:
                all_pages_tasks = [get_page(session, i)
                                   for i in range(total_pages)]
                # fetching all pages
                all_pages = await tqdm.gather(*all_pages_tasks)
                all_terms = [
                    term for page in all_pages for term in page["_embedded"]["terms"]]  # creating a list of all fetched terms

                all_parents_tasks = []
                for term in all_terms[:total_items]:
                    if "parents" in term["_links"]:
                        all_parents_tasks.append(get_term_parents(
                            session, term["_links"]["parents"]["href"]))
                    else:
                        all_parents_tasks.append(get_none())
                all_parents_data = await tqdm.gather(*all_parents_tasks)

                # creating all new terms and synonyms
                create_all_terms_tasks = [
                    create_term_task(term) for term in all_terms]
                created_terms = await tqdm.gather(*create_all_terms_tasks)
                terms_mapping = {term.id: term for term in created_terms}
    
                # creating ontology relationships
                create_all_ontologies_tasks = [
                    create_ontology_task(term, all_parents_data[i], terms_mapping) for i, term in enumerate(created_terms)
                ]
                await tqdm.gather(*create_all_ontologies_tasks)

        asyncio.run(main())
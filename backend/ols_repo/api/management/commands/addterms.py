from django.core.management.base import BaseCommand
import requests
from api.models import Term, Synonym
import aiohttp
import asyncio
from aiohttp.client_exceptions import ServerDisconnectedError
from tqdm.asyncio import tqdm


async def get_term_parents(session, url):
    """
    Fetcher function for term parents.
    If the call initially fails due to load,
    we retry after 5 seconds.
    """
    fetched = False
    while not fetched:
        try:
            async with session.get(url) as resp:
                fetched = True
                page = await resp.json()
                return page
        except ServerDisconnectedError:
            await asyncio.sleep(5)


async def get_page(session, page_index):
    """
    Fetcher function for term pages.
    """
    async with session.get(f"https://www.ebi.ac.uk/ols/api/ontologies/efo/terms?page={page_index}&size=500") as resp:
        page = await resp.json()
        return page


async def create_term_task(term):
    """
    async function that creates Term models and their synonyms as needed.
    """
    new_term = await Term.objects.acreate(  # creating and saving the new term
        label=term["label"], description="".join(term["description"]), id=term["short_form"])
    for synonym in term["synonyms"]:
        try:
            # saving each synonym
            synonym_query_result = await Synonym.objects.aget_or_create(label=synonym)
            await new_term.synonyms.aadd(synonym_query_result[0])
        except:
            pass
    return new_term


async def create_ontology_task(term, parents, mapping):
    """
    async function that creates parent-child relationships.
    """
    if parents:
        for parent in parents["_embedded"]["terms"]:
            try:
                new_ontology_relationship = await term.parents.aadd(mapping[parent["short_form"]])
            except:
                pass


async def get_none():
    """
    async function that does nothing. Used as a placeholder below.
    """
    return None


class Command(BaseCommand):
    help = "Fetches terms from the OLS API and populates the DB"

    async def run_with_log(self, label, tasks):
        """
        just a wrapper for async tasks with a progress bar and messages
        """
        self.stdout.write(
            self.style.NOTICE(f'{label} start')
        )
        completed_tasks = await tqdm.gather(*tasks)
        self.stdout.write(
            self.style.SUCCESS(f'{label} success')
        )
        return completed_tasks

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("term_limit", nargs="?", type=int)

    def handle(self, *args, **options):
        upper_limit = options["term_limit"]
        Term.objects.all().delete()
        Synonym.objects.all().delete()

        # fetching this only to get pagination data
        initial_data_request = requests.get(
            "https://www.ebi.ac.uk/ols/api/ontologies/efo/terms")
        initial_data = initial_data_request.json()

        pagination_data = initial_data["page"]
        total_items = upper_limit or pagination_data["totalElements"]
        # 500 is the upper limit for items per page on the API
        total_pages = total_items // 500 + 1
        last_page_remainder = total_items % 500
        if last_page_remainder == 0:
            total_pages -= 1

        async def main():
            async with aiohttp.ClientSession() as session:

                # fetching all pages
                all_pages_tasks = [get_page(session, i)
                                   for i in range(total_pages)]
                all_pages = await self.run_with_log("pages", all_pages_tasks)

                all_terms = [
                    term for page in all_pages for term in page["_embedded"]["terms"]]  # creating a list of all fetched terms

                # fetching all parents
                all_parents_tasks = []
                for term in all_terms[:total_items]:
                    if "parents" in term["_links"]:
                        all_parents_tasks.append(get_term_parents(
                            session, term["_links"]["parents"]["href"]))
                    else:
                        # if the term has no parent, we insert just a placeholder
                        # this allows us to use the same index for terms and their parents
                        # and check if parent exists/is not None later on
                        all_parents_tasks.append(get_none())

                all_parents_data = await self.run_with_log("parents", all_parents_tasks)

                # creating all new terms and synonyms
                create_all_terms_tasks = [
                    create_term_task(term) for term in all_terms[:total_items]]
                created_terms = await self.run_with_log("Save terms and synonyms", create_all_terms_tasks)
                terms_mapping = {term.id: term for term in created_terms}

                # creating ontology relationships
                create_all_ontologies_tasks = [
                    create_ontology_task(term, all_parents_data[i], terms_mapping) for i, term in enumerate(created_terms)
                ]
                await self.run_with_log("create ontology rels", create_all_ontologies_tasks)

        asyncio.run(main())  # our entry point

from classifieds.classified import Classified
from craigslist import CraigslistForSale
import time
import re
import progressbar
import os
from typing import Dict


class CraigslistSearchParams:
    def __init__(self, min_price=None, max_price=None, title=None, category=None):
        assert category is not None and len(
            category) > 0, ("Craigslist category must not be null")
        self.title = title
        self.min_price = min_price
        self.max_price = max_price
        self.category = category

    title = ""
    min_price = None
    max_price = None


class Craigslist(object):
    cities = []

    def __init__(self):
        with open(
            os.path.join(os.path.dirname(
                os.path.realpath(__file__)), "./cities.dat"), "r"
        ) as city_file:
            for l in city_file:
                self.cities.append(l.rstrip())

    def __get_listings_for_city(self, city, search_filter: CraigslistSearchParams):
        try:
            cl = CraigslistForSale(
                site=city,
                category=search_filter.category,
                filters={
                    "max_price": search_filter.max_price,
                    "min_price": search_filter.min_price,
                    "query": search_filter.title,
                    "search_titles": True,
                },
            ).get_results(include_details=True)
            return cl
        except ValueError:
            print("invalid site {}".format(city))
            return []

    @staticmethod
    def __classified_search_params_to_craigslist_params(
        classified_search_params: Dict,
    ) -> CraigslistSearchParams:
        return CraigslistSearchParams(
            category=classified_search_params['craigslist_category'],
            min_price=classified_search_params.get('min_price'),
            max_price=classified_search_params.get('max_price'),
            title=classified_search_params['title'],
        )

    @staticmethod
    def __craigslist_listing_to_airplane(listing):
        return Classified(
            url=listing["url"],
            price=int(re.sub("[^0-9]", "", listing["price"])),
            title=listing["name"],
            description=listing["body"],
        )

    def search(self, search_params: Dict = {}):
        craigslist_params = Craigslist.__classified_search_params_to_craigslist_params(
            search_params
        )
        listing_results = []
        with progressbar.ProgressBar(max_value=len(self.cities)) as bar:
            for city in self.cities[:1]:
                time.sleep(1)
                current_results = [
                    Craigslist.__craigslist_listing_to_airplane(listing)
                    for listing in self.__get_listings_for_city(city, craigslist_params)
                ]
                listing_results = listing_results + current_results
                bar.update(self.cities.index(city))

        return [result for result in listing_results if result is not None]

from ..plane_repository import PlaneSearchParams, PlaneRepository
from planes.models import Airplane
from craigslist import CraigslistForSale
import time
import re
from django.db import IntegrityError


class CraigslistSearchParams:
    def __init__(self, min_price=None, max_price=None, title=None):
        self.title = title
        self.min_price = min_price
        self.max_price = max_price

    title = ''
    min_price = None
    max_price = None


class Craigslist(PlaneRepository):
    cities = []

    def __init__(self):
        with open('planes/repositories/plane/craigslist_repository/cities.txt', 'r') as city_file:
            for l in city_file:
                self.cities.append(l.rstrip())

    def __get_listings_for_city(self, city, search_filter: CraigslistSearchParams):
        try:
            cl = CraigslistForSale(site=city, category='ava', filters={
                'max_price': search_filter.max_price,
                'min_price': search_filter.min_price,
                'query': search_filter.title,
                'search_titles': True
            }).get_results(include_details=True)
            return cl
        except ValueError:
            print('invalid site {}'.format(city))
            return []

    @staticmethod
    def __plane_search_params_to_craigslist_params(plane_search_params: PlaneSearchParams):
        return CraigslistSearchParams(min_price=plane_search_params.price_gte, max_price=plane_search_params.price_lte, title=plane_search_params.title)

    @staticmethod
    def __craigslist_listing_to_airplane(listing):
        try:
            return Airplane.objects.create(
                url=listing['url'],
                price=int(re.sub("[^0-9]", "", listing['price'])),
                title=listing['name'],
                description=listing['body']
            )
        except IntegrityError:
            print('plane already exists')

    def search(self, search_params: PlaneSearchParams = PlaneSearchParams()):
        craigslist_params = Craigslist.__plane_search_params_to_craigslist_params(
            search_params)
        listing_results = []
        for city in self.cities[:30]:
            time.sleep(0.2)
            print('searching city: {city}'.format(city=city))
            current_results = [Craigslist.__craigslist_listing_to_airplane(
                listing) for listing in self.__get_listings_for_city(city, craigslist_params)]
            listing_results = listing_results + current_results
            for result in current_results:
                print(result)
        return listing_results

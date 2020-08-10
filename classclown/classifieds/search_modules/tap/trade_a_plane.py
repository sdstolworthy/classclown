from typing import Text, Dict
from bs4 import BeautifulSoup, PageElement
import requests
import re
from classifieds.classified import Classified


class TradeAPlaneSearchParams:
    keyword: Text
    max_price: int
    min_price: int

    def __init__(self, keyword="", max_price=None, min_price=None):
        self.max_price = max_price
        self.min_price = min_price
        self.title = keyword


class TradeAPlaneListing:
    title: Text = ""
    price: float = None
    description: Text = ""
    url: Text = ""

    def __init__(self, title='', price=None, description='', url=None):
        self.title = title
        self.price = price
        self.description = description
        self.url = url

    @staticmethod
    def faked():
        listing = TradeAPlaneListing()
        listing.title = "Faked Classified Title"
        listing.description = "Faked Classified Description"
        listing.price = 10000
        return listing

    def __str__(self):
        return "Trade-A-Classified: Listing: ${} for {}".format(self.price, self.title)


class TradeAPlane:
    base_url = "https://trade-a-plane.com"

    def __classified_to_airplane(self, classified: TradeAPlaneListing):
        return Classified(
            price=classified.price,
            title=classified.title,
            description=classified.description,
            url=classified.url,
        )

    def __classified_search_params_to_tap_params(
        self, search_param:  Dict = {}
    ):
        return TradeAPlaneSearchParams(
            keyword=search_param['title'],
            min_price=search_param.get('min_price'),
            max_price=search_param.get('max_price'),
        )

    def __get_search_url(self, search_params: TradeAPlaneSearchParams = TradeAPlaneSearchParams()):
        base_search_url = self.base_url + '/filtered/search?s-type=aircraft&s-advanced=yes&sale_status=For+Sale&category_level1=Single+Engine+Piston&price-min={min_price}&price-max={max_price}&user_distance=1000000'.format(
            max_price=search_params.max_price if search_params.max_price is not None else '',
            min_price=search_params.min_price if search_params.min_price is not None else ''
        )
        if search_params.title is not None and len(search_params.title.strip()) > 0:
            base_search_url += '&s-keyword-search={keyword}'.format(
                keyword=search_params.title)
        return base_search_url

    def __parse_result_item(self, result_item: PageElement):
        result_title = result_item.find_next(id='title')
        price_text = re.sub(
            "[^0-9]", "", result_item.find_next(class_='txt-price').text)
        price = 0
        description = result_item.find_next(class_='description').text.strip()
        url = self.base_url + result_title['href']
        if len(price_text) != 0:
            price = int(price_text)
        return TradeAPlaneListing(title=result_title.text.strip(), price=price, description=description, url=url)

    def __parse_results_page(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        next_link = soup.find(
            lambda tag: tag.name == "a" and ">" in tag.text)
        page_results = [self.__parse_result_item(
            item) for item in soup.find_all(class_='result_listing')]
        if next_link is not None:
            next_link = self.base_url + next_link['href']
        return page_results, next_link

    def search(self, search_params: Dict = {}):
        tap_search_params = self.__classified_search_params_to_tap_params(
            search_params
        )
        next_link = self.__get_search_url(
            search_params=tap_search_params)
        found_listings = []
        prev_link = ''
        while next_link is not None and next_link != prev_link:
            page = requests.get(next_link)
            prev_link = next_link
            listings, next_link = self.__parse_results_page(page.text)
            found_listings += listings
        airplanes = [
            self.__classified_to_airplane(classified) for classified in found_listings
        ]
        classifieds = [
            airplane for airplane in airplanes if airplane is not None]
        return classifieds

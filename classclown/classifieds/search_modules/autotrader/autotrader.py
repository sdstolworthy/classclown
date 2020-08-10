from typing import Dict, List, Text
from classifieds.classified import Classified


class AutotraderSearchParams:

    make: List[Text] = []
    model: List[Text] = []
    min_price: int = 0
    max_price: int = 9999999
    zip_code: Text = "37064"
    search_radius: int = 100


class Autotrader:
    search_params: AutotraderSearchParams = AutotraderSearchParams()
    base_url = "https://autotrader.com"

    def __search_dict_to_autotrader_params(self, param_dict: Dict = {}) -> AutotraderSearchParams:
        params = AutotraderSearchParams()
        params.make = param_dict.get('make')
        params.model = param_dict.get('model')
        params.min_price = param_dict.get('min_price')
        params.max_price = param_dict.get('max_price')
        params.zip_code = param_dict.get('zip_code')
        params.radius = param_dict.get('radius')
        return params

    def __parse_listing_page(self):
        pass

    def __scrape(self, start_url) -> List[Classified]:
        pass

    def __compile_url_from_params(self):
        return self.base_url + ""

    def search(self, param_dict={}) -> List[Classified]:
        self.search_params = self.__search_dict_to_autotrader_params(
            param_dict)
        request_url = self.__compile_url_from_params()
        print(request_url)

        return []

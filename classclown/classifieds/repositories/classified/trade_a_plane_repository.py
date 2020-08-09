from .classified_repository import ClassifiedRepository, ClassifiedSearchParams
from classclown.classifieds.models import Classified
from typing import Text
from django.db import IntegrityError
from tap.trade_a_classified import TradeAClassifiedListing, TradeAClassifiedSearchParams, TradeAClassified


class TradeAClassifiedRepository(ClassifiedRepository):
    def __classified_to_airclassified(self, classified: TradeAClassifiedListing):
        try:
            return Classified.objects.create(
                price=classified.price,
                title=classified.title,
                description=classified.description,
                url=classified.url,
            )
        except IntegrityError:
            pass

    def __classified_search_params_to_barnstormer_params(
        self, search_param: ClassifiedSearchParams = ClassifiedSearchParams()
    ):
        return TradeAClassifiedSearchParams(
            keyword=search_param.title,
            min_price=search_param.price_gte,
            max_price=search_param.price_lte,
        )

    def search(self, search_param: ClassifiedSearchParams = ClassifiedSearchParams()):
        barnstormer_search_params = self.__classified_search_params_to_barnstormer_params(
            search_param
        )
        classifieds = TradeAClassified().search(barnstormer_search_params)
        classifieds = [
            self.__classified_to_airclassified(classified) for classified in classifieds
        ]
        classifieds = [airclassified for airclassified in classifieds if airclassified is not None]
        return classifieds

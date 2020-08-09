from .classified_repository import ClassifiedRepository, ClassifiedSearchParams
from classclown.classifieds.models import Classified
from django.db import IntegrityError
from classclown.search_modules.barnstormers.barnstormers import (
    BarnstormersClassifiedListing,
    BarnstormerSearchParams,
    Barnstormers,
)


class BarnstormersClassifiedRepository(ClassifiedRepository):
    def __classified_to_airclassified(self, classified: BarnstormersClassifiedListing):
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
        return BarnstormerSearchParams(
            keyword=search_param.title,
            price_gte=search_param.price_gte,
            price_lte=search_param.price_lte,
        )

    def search(self, search_param: ClassifiedSearchParams = ClassifiedSearchParams()):
        barnstormer_search_params = self.__classified_search_params_to_barnstormer_params(
            search_param
        )
        serialized_classifieds = [
            self.__classified_to_airclassified(listing)
            for listing in Barnstormers().classifieds.search(barnstormer_search_params)
        ]
        classifieds = [
            airclassified for airclassified in serialized_classifieds if airclassified is not None
        ]
        return classifieds

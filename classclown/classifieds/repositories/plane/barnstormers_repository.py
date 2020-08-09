from .plane_repository import PlaneRepository, PlaneSearchParams
from classclown.classifieds.models import Classified
from typing import Text
from django.db import IntegrityError
from barnstormers.barnstormers import (
    BarnstormersClassifiedListing,
    BarnstormerSearchParams,
    Barnstormers,
)


class BarnstormersPlaneRepository(PlaneRepository):
    def __classified_to_airplane(self, classified: BarnstormersClassifiedListing):
        try:
            return Classified.objects.create(
                price=classified.price,
                title=classified.title,
                description=classified.description,
                url=classified.url,
            )
        except IntegrityError:
            pass

    def __plane_search_params_to_barnstormer_params(
        self, search_param: PlaneSearchParams = PlaneSearchParams()
    ):
        return BarnstormerSearchParams(
            keyword=search_param.title,
            price_gte=search_param.price_gte,
            price_lte=search_param.price_lte,
        )

    def search(self, search_param: PlaneSearchParams = PlaneSearchParams()):
        barnstormer_search_params = self.__plane_search_params_to_barnstormer_params(
            search_param
        )
        serialized_classifieds = [
            self.__classified_to_airplane(listing)
            for listing in Barnstormers().classifieds.search(barnstormer_search_params)
        ]
        classifieds = [
            airplane for airplane in serialized_classifieds if airplane is not None
        ]
        return classifieds

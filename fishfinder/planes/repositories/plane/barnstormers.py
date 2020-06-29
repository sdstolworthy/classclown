from .plane_repository import PlaneRepository, PlaneSearchParams
from planes.models import Airplane
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
            return Airplane.objects.create(
                price=classified.price,
                title=classified.title,
                description=classified.description,
                url=classified.url,
            )
        except IntegrityError:
            print("Value already exists")

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
        classifieds = Barnstormers().classifieds.search(barnstormer_search_params)
        airplanes = [self.__classified_to_airplane(
            listing) for listing in classifieds]
        for airplane in airplanes:
            print(airplane)
        return airplanes

from ._step import PipelineStep
from classclown.classifieds.models import Classified
from typing import List
from classifieds.repositories.classified.classified_repository import (
    ClassifiedRepository,
    ClassifiedSearchParams,
)


class Search(PipelineStep):
    classified_repository: ClassifiedRepository
    search_params = None

    def __init__(
        self,
        classified_repository: ClassifiedRepository,
        search_params=ClassifiedSearchParams(),
        name="",
    ):
        if classified_repository is None:
            raise ValueError("Classified Repository must not be null")
        self.classified_repository = classified_repository
        self.search_params = search_params
        super().__init__(name)

    def execute(self, _) -> List[Classified]:
        classifieds = self.classified_repository.search(self.search_params)
        return classifieds


from ._step import PipelineStep
from classifieds.models import Classified
from typing import List


class Search(PipelineStep):
    search_module = None
    search_params = None

    def __init__(
        self,
        search_module,
        search_params=None,
        name="",
    ):
        search_params = search_params if search_params is not None else {}
        if search_module is None:
            raise ValueError("Classified Repository must not be null")
        self.search_module = search_module
        self.search_params = search_params
        super().__init__(name)

    def execute(self, _) -> List[Classified]:
        classifieds = self.search_module.search(self.search_params)
        return classifieds

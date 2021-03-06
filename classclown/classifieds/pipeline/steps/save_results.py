from ._step import PipelineStep
from classifieds.models import Classified
from typing import List


class SaveStep(PipelineStep):
    def __init__(self):
        super().__init__("Save Step")

    def execute(self, previous_results: List[Classified]):
        for result in previous_results:
            Classified.save_classified(result)
        return previous_results

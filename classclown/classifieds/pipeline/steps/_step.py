from classifieds.models.classified import Classified


class PipelineStep:
    name = ""

    def __init__(self, name=""):
        self.name = name

    def execute(self, previous_results: [Classified] = []):
        raise NotImplementedError()

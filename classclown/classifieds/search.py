from classifieds.models import Classified
from classifieds.pipeline.pipeline import ClassifiedSearchPipeline


def run():
    ClassifiedSearchPipeline().run()

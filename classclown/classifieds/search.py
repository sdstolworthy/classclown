from classclown.classifieds.models import Classified
from classclown.classifieds.pipeline.pipeline import ClassifiedSearchPipeline


def run():
    ClassifiedSearchPipeline().run()

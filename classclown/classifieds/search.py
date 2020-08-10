import os
from classifieds.models import Classified
from classifieds.pipeline.pipeline import ClassifiedSearchPipeline
from .config_loader import load_config


def run():
    config = load_config(os.environ.get('CONFIG_LOCATION'))
    ClassifiedSearchPipeline(config).run()

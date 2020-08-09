from .steps import search, save_results
from classifieds.search_params import ClassifiedSearchParams
from classifieds.search_modules.barnstormers import Barnstormers
from classifieds.search_modules.tap import TradeAPlane
from classifieds.search_modules.craigslist import Craigslist

import time


class ClassifiedSearchPipeline:
    search_filter = ClassifiedSearchParams(price_gte=20000, price_lte=40000)
    pipeline = [
        search.Search(
            Barnstormers(), search_filter, name="Barnstormer Search"
        ),
        search.Search(Craigslist(), search_filter, name="Craigslist Search"),
        search.Search(
            TradeAPlane(), search_filter, name="TradeAClassified Search"
        ),
    ]

    def run(self):
        print("running")
        running_results = []
        pipeline_start_time = time.time()
        for step in self.pipeline:
            start_time = time.time()
            print("{}: started".format(step.name))
            running_results = running_results + [
                step_result
                for step_result in step.execute(running_results)
                if step_result is not None
            ]
            end_time = time.time()
            print(
                "{}: completed in {} seconds".format(
                    step.name, round(end_time - start_time)
                )
            )
        pipeline_end_time = time.time()
        for result in running_results:
            print(result)
        print(
            "Found {} {} in {} seconds".format(
                len(running_results),
                "classifieds" if len(running_results) != 1 else "classified",
                round(pipeline_end_time - pipeline_start_time),
            ),
        )

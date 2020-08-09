from typing import Text
from faker import Faker

fake = Faker()


class Classified(object):
    price: int = None
    description: Text = None
    city: Text = None
    url: Text = None
    title: Text = None

    def __init__(self, price=None, description=None, city=None, url=None, title=None) -> None:
        self.price = price
        self.description = description
        self.city = city
        self.url = url
        self.title = title

    @staticmethod
    def faked():
        return Classified(price=fake.random_int(1000, 12000))

    def __str__(self):
        return "Classified: {} for ${} at {url}".format(
            self.title, self.price, url=self.url
        )

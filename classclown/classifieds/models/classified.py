from django.db import models
from faker import Faker
from .base import BaseModel
from ..classified import Classified as PyClassified

fake = Faker()


class Classified(BaseModel):

    price = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    url = models.TextField(blank=False, null=False, unique=True)
    title = models.TextField(blank=True, null=True)

    @staticmethod
    def faked():
        return Classified(price=fake.random_int(1000, 12000))

    def __str__(self):
        return "Classified: {} for ${} at {url}".format(
            self.title, self.price, url=self.url
        )

    @staticmethod
    def save_classified(classified: PyClassified):
        return Classified.objects.create(
            price=classified.price,
            description=classified.description,
            city=classified.city,
            url=classified.url,
            title=classified.title
        )

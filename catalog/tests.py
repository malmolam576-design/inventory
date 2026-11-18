from django.http import QueryDict
from django.test import TestCase

from catalog.filters import ProductFilter
from catalog.models import Category, Product, Tag


class ProductFilterTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tools = Category.objects.create(name="Tools", slug="tools")
        cls.toys = Category.objects.create(name="Toys", slug="toys")
        cls.red = Tag.objects.create(name="Red", slug="red")
        cls.big = Tag.objects.create(name="Big", slug="big")

        cls.hammer = Product.objects.create(name="Hammer", price=10, category=cls.tools)
        cls.hammer.tags.add(cls.red, cls.big)
        cls.robot = Product.objects.create(name="Robot", price=20, category=cls.toys)
        cls.robot.tags.add(cls.red)
        cls.saw = Product.objects.create(name="Saw", price=15, category=cls.tools)

    def run_filter(self, query=""):
        product_filter = ProductFilter(QueryDict(query))
        return list(product_filter.apply(Product.objects.all()))

    def test_tag_filter(self):
        self.assertEqual(self.run_filter("tag=red"), [self.hammer, self.robot])

    def test_category_filter(self):
        self.assertEqual(self.run_filter("category=tools"), [self.hammer, self.saw])

    def test_category_and_tag_filter(self):
        self.assertEqual(self.run_filter("category=tools&tag=red"), [self.hammer])

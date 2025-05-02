from django.test import TestCase
from products.models import Category, Product


class CategoryModelTest(TestCase):
    def test_string_representation(self):
        category = Category.objects.create(name='jackets')
        self.assertEqual(str(category), 'jackets')

    def test_get_friendly_name(self):
        category = Category.objects.create(name='pants', friendly_name='Pants')
        self.assertEqual(category.get_friendly_name(), 'Pants')

    def test_default_stretch_factors(self):
        category = Category.objects.create(name='tops')
        self.assertEqual(category.slim_factor, 1.00)
        self.assertEqual(category.regular_factor, 1.10)
        self.assertEqual(category.loose_factor, 1.20)


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='coats')

    def test_string_representation(self):
        product = Product.objects.create(
            category=self.category,
            name='Rain Coat',
            description='A waterproof rain coat.',
            price=99.99
        )
        self.assertEqual(str(product), 'Rain Coat')

    def test_product_creation_with_minimal_fields(self):
        product = Product.objects.create(
            category=self.category,
            name='Test Product',
            description='Test description',
            price=49.99
        )
        self.assertFalse(product.has_sizes)
        self.assertIsNone(product.image_url)
        self.assertFalse(product.image)

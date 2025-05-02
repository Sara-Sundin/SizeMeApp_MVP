from django.test import TestCase
from products.models import Category, Product
from sizemeapp.models import GarmentFit

class GarmentFitModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="tshirts", friendly_name="T-Shirts")
        self.product = Product.objects.create(
            name="Test Tee",
            description="Comfortable cotton t-shirt.",
            price=25.00,
            category=self.category
        )

    def test_create_garment_fit(self):
        fit = GarmentFit.objects.create(product=self.product, size_label="M", chest=96.5)
        self.assertEqual(str(fit), "Test Tee - M (Chest: 96.5cm)")
        self.assertEqual(fit.product, self.product)
        self.assertEqual(fit.size_label, "M")
        self.assertEqual(fit.chest, 96.5)

    def test_unique_together_constraint(self):
        GarmentFit.objects.create(product=self.product, size_label="L", chest=101.0)
        with self.assertRaises(Exception):
            # Should raise IntegrityError due to unique_together constraint
            GarmentFit.objects.create(product=self.product, size_label="L", chest=102.0)

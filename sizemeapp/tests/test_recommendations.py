from django.test import TestCase
from decimal import Decimal
from products.models import Category, Product
from sizemeapp.models import GarmentFit
from sizemeapp.utils.recommendations import get_size_recommendations


class SizeRecommendationTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="tshirts",
            friendly_name="T-Shirts",
            slim_factor=Decimal("1.00"),
            regular_factor=Decimal("1.10"),
            loose_factor=Decimal("1.20"),
        )

        self.product = Product.objects.create(
            name="SizeTest Tee",
            description="Test product",
            price=25.00,
            category=self.category,
        )

        # Add some garment fits (sizes)
        GarmentFit.objects.create(product=self.product, size_label="S", chest=Decimal("90.0"))
        GarmentFit.objects.create(product=self.product, size_label="M", chest=Decimal("100.0"))
        GarmentFit.objects.create(product=self.product, size_label="L", chest=Decimal("110.0"))

    def test_recommendation_returns_sizes(self):
        user_chest = Decimal("100.0")
        recs = get_size_recommendations(user_chest, self.product)
        self.assertTrue(any(r["size_label"] == "M" for r in recs))
        self.assertGreaterEqual(len(recs), 2)


    def test_recommendation_handles_no_category(self):
        self.product.category = None
        self.product.save()

        # Add fits to ensure fallback logic is tested
        GarmentFit.objects.all().delete()
        GarmentFit.objects.create(product=self.product, size_label="S", chest=Decimal("95.0"))
        GarmentFit.objects.create(product=self.product, size_label="M", chest=Decimal("104.5"))
        GarmentFit.objects.create(product=self.product, size_label="L", chest=Decimal("114.0"))

        recs = get_size_recommendations(Decimal("95.0"), self.product)
        self.assertEqual(len(recs), 3)

    def test_recommendation_filters_out_far_matches(self):
        GarmentFit.objects.all().delete()  # Remove all sizes
        GarmentFit.objects.create(product=self.product, size_label="XXL", chest=Decimal("150.0"))
        recs = get_size_recommendations(Decimal("90.0"), self.product)
        self.assertEqual(len(recs), 0)  # too far off

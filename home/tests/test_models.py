from django.test import TestCase
from home.models import Plan


class PlanModelTest(TestCase):

    def setUp(self):
        self.plan = Plan.objects.create(
            name="Growth Plan",
            plan_type="growth",
            monthly_price=49.99,
            setup_cost=199.00,
            short_description="For growing teams",
            long_description="A longer description of the Growth Plan.",
            features="Feature A\nFeature B\nFeature C",
            perfect_for="Teams with 5-20 people",
            icon_class="fa-chart-line",
            icon_color_class="text-success",
            button_class="btn-primary",
        )

    def test_plan_str_returns_name(self):
        self.assertEqual(str(self.plan), "Growth Plan")

    def test_feature_list_splits_lines(self):
        expected_features = ["Feature A", "Feature B", "Feature C"]
        self.assertEqual(self.plan.feature_list(), expected_features)

    def test_optional_fields_can_be_blank(self):
        plan = Plan.objects.create(
            name="Starter Plan",
            plan_type="starter",
            monthly_price=0,
            setup_cost=0,
            short_description="Free tier",
            long_description="Best for testing",
            features="Basic Feature 1",
        )
        self.assertIsNone(plan.perfect_for)
        self.assertEqual(plan.icon_class, "")
